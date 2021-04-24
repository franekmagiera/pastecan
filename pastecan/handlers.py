from aiohttp import web
from datetime import datetime, timedelta
import jwt
from json import dumps
from jsonschema import validate
import oauthlib.oauth1
from sqlalchemy import and_, desc, func, or_, select
from yarl import URL

from db import transaction_context, pastes_table, login_sessions_table, users_table
from json_schema import post_pastes_schema
from mock_data import jane, john
from settings import STATIC_DIR

LANGUAGE_OPTIONS = ['none', 'clike', 'java', 'javascript', 'python', 'scala', 'scheme', 'typescript']
MAX_CONTENT_LENGTH = 20000
TOKEN_COOKIE = 'token'


def _first_line(string):
    return string.split('\n')[0]


def _get_claims(cookies, jwt_key, jwt_algorithm):
    # Returns a pair consisting of user_id and screen_name.

    token = cookies.get(TOKEN_COOKIE)
    if token is not None:
        try:
            claims = jwt.decode(token, key=jwt_key, algorithms=jwt_algorithm)
            user_id = claims.get('userId')
            screen_name = claims.get('screenName')
        except jwt.ExpiredSignature:
            raise web.HTTPBadRequest('Session expired, please try logging out and loggin in again')
        except jwt.InvalidSignatureError:
            raise web.HTTPBadRequest('Could not verify user identity')
    else:
        user_id = None
        screen_name = None
    return user_id, screen_name


with open(STATIC_DIR / 'index.html') as index_file:
    index_html = index_file.read()


async def get_index(request):
    return web.Response(body=index_html, content_type='text/html')


def _verify_body(body):
    # Raises an error if request body for PUT or POST request violates API contract.

    try:
        validate(instance=body, schema=post_pastes_schema)
    except Exception as e:
        raise web.HTTPBadRequest(f'Wrong body structure:\n{_first_line(str(e))}')

    if body['language'] not in LANGUAGE_OPTIONS:
        raise web.HTTPBadRequest(f'''Unsupported language: {body['language']}''')
    if len(body['content']) > MAX_CONTENT_LENGTH:
        raise web.HTTPBadRequest(f'Paste exceeding maximum length of {MAX_CONTENT_LENGTH}')
    if not ''.join(body['content'].split()):
        raise web.HTTPBadRequest(f'Paste cannot be empty')
    if not (body['exposure'] == 'Public' or body['exposure'] == 'Private'):
        raise web.HTTPBadRequest('Paste exposure can only be "Public" or "Private"')


async def _should_authorize(conn, paste_id, cookies, jwt_key, jwt_algorithm):
    # Raises an error if the request should not be processed.
    
    pastes = await conn.execute(pastes_table.select().where(pastes_table.c.id == paste_id))
    paste = await pastes.first()
    if paste is None:
        raise web.HTTPNotFound()
    user_id, _ = _get_claims(cookies, jwt_key, jwt_algorithm)
    if user_id is None or user_id != paste['user_id']:
        raise web.HTTPForbidden()


def _create_token(user_id, user_screen_name, jwt_key, jwt_algorithm):
    expiration_date = datetime.now() + timedelta(1)  # Expires in 24h.
    jwt_key = jwt_key
    jwt_algorithm = jwt_algorithm
    encoded = jwt.encode({
        'iss': 'pastecan',
        'exp': int(expiration_date.timestamp()),
        'userId': user_id,
        'screenName': user_screen_name
    }, key=jwt_key, algorithm=jwt_algorithm)
    return encoded


async def post_paste(request):
    body = await request.json()
    _verify_body(body)

    body['title'] = body['title'] or 'Untitled'
    date = datetime.now()
    user_id, _ = _get_claims(request.cookies, request.app['jwt_key'], request.app['jwt_algorithm'])

    if body['exposure'] == 'Private' and user_id is None:
        raise web.HTTPBadRequest('Cannot create a private paste while not logged in')

    async with request.app['db_engine'].acquire() as conn:
        async with transaction_context(conn) as tc_conn:
            await tc_conn.execute(pastes_table.insert().values(date=date, user_id=user_id, **body))
            new_id = await tc_conn.execute('SELECT LAST_INSERT_ID();')

    new_id = await new_id.scalar()

    return web.json_response({'id': new_id})


async def put_paste(request):
    body = await request.json()
    _verify_body(body)
    paste_id = request.match_info['id']

    async with request.app['db_engine'].acquire() as conn:
        await _should_authorize(conn, paste_id, request.cookies, request.app['jwt_key'], request.app['jwt_algorithm'])
        async with transaction_context(conn) as tc_conn:
            await tc_conn.execute(pastes_table.update().where(pastes_table.c.id == paste_id).values(**body))
    return web.HTTPNoContent()



async def get_pastes(request):
    params = request.query
    offset = int(params['offset']) if 'offset' in params else None
    limit = int(params['limit']) if 'limit' in params else None
    if limit is None and offset is not None:
        raise web.HTTPBadRequest('Limit must be provided if offset was provided')
    user = params.get('user')

    user_id, screen_name = _get_claims(request.cookies, request.app['jwt_key'], request.app['jwt_algorithm'])

    joined_tables = pastes_table.outerjoin(users_table, pastes_table.c.user_id == users_table.c.user_id)

    query = select(
        pastes_table.c.id,
        pastes_table.c.title,
        pastes_table.c.language,
        pastes_table.c.date,
        pastes_table.c.exposure,
        users_table.c.screen_name.label('screenName')
    ).select_from(joined_tables)

    count_query = select(func.count(pastes_table.c.id)).select_from(joined_tables)

    filter_expression = None
    if user is None and user_id is None:
        # Fetch all public pastes.
        filter_expression = pastes_table.c.exposure == 'Public'
    elif user is None and user_id is not None:
        # Fetch public and private pastes of the requestee pastes and all public pastes.
        filter_expression = or_(pastes_table.c.exposure == 'Public', pastes_table.c.user_id == user_id)
    elif user == screen_name:
        # Fetch all pastes of `user`.
        filter_expression = pastes_table.c.user_id == user_id
    elif user != screen_name:
        # Fetch all public pastes of `user`.
        filter_expression = and_(users_table.c.screen_name == user, pastes_table.c.exposure == 'Public')
    
    query = query.order_by(desc(pastes_table.c.date)).where(filter_expression)
    count_query = count_query.where(filter_expression)
    if limit is not None:
        query = query.limit(limit)
        count_query = count_query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
        count_query = count_query.offset(offset)


    async with request.app['db_engine'].acquire() as conn:
        pastes = await conn.execute(query)
        count = await conn.execute(count_query)

    pastes = await pastes.fetchall()
    pastes = [{column: value for column, value in row.items()} for row in pastes]
    count = await count.scalar()

    return web.json_response({
        'items': pastes,
        'count': count
    },
    dumps=lambda data: dumps(data, default=str))


async def get_paste(request):
    paste_id = request.match_info['id']
    async with request.app['db_engine'].acquire() as conn:
        pastes = await conn.execute(pastes_table.select().where(pastes_table.c.id == paste_id))
        paste = await pastes.first()
        if paste is None:
            raise web.HTTPNotFound()
        paste = {column: value for column, value in paste.items()}
        if paste['exposure'] == 'Private':
            user_id, _ = _get_claims(request.cookies, request.app['jwt_key'], request.app['jwt_algorithm'])
            if user_id is None:
                raise web.HTTPForbidden('Try logging in to see private resources')
            elif user_id != paste['user_id']:
                raise web.HTTPForbidden()
        # Paste is public or user provided a valid token with a valid id.
        screen_name = None
        if paste['user_id'] is not None:
            screen_names = await conn.execute(select(users_table.c.screen_name).select_from(users_table).where(users_table.c.user_id == paste['user_id']))
            screen_name = await screen_names.first()
            screen_name = screen_name[0]
    del paste['user_id']
    paste['screenName'] = screen_name
    return web.json_response(paste, dumps=lambda data: dumps(data, default=str))


async def delete_paste(request):
    paste_id = request.match_info['id']
    async with request.app['db_engine'].acquire() as conn:
        await _should_authorize(conn, paste_id, request.cookies, request.app['jwt_key'], request.app['jwt_algorithm'])
        async with transaction_context(conn) as tc_conn:
            await tc_conn.execute(pastes_table.delete().where(pastes_table.c.id == paste_id))
    return web.HTTPNoContent()


async def twitter_login(request):
    twitter_api_key = request.app['twitter_api_key']
    twitter_api_secret_key = request.app['twitter_api_secret_key']
    twitter_oauth_callback = request.app['twitter_oauth_callback']
    request_token_endpoint = request.app['request_token_endpoint']
    authenticate_endpoint = request.app['authenticate_endpoint']

    client = oauthlib.oauth1.Client(twitter_api_key, client_secret=twitter_api_secret_key, callback_uri=twitter_oauth_callback)
    uri, headers, _ = client.sign(request_token_endpoint, http_method='POST')

    session = request.app['client_session']
    
    # Fetch an anauthorized request token.
    async with session.post(uri, headers=headers) as response:
        if response.status != 200:
            raise web.HTTPInternalServerError()
        body = await response.text()

    # Parse oauth_token, oauth_token_secret, oauth_callback_confirmed.
    body = dict([pair.split('=') for pair in body.split('&')])

    if body.get('oauth_callback_confirmed') != 'true':
        raise web.HTTPInternalServerError()

    oauth_token = body['oauth_token']
    oauth_token_secret = body['oauth_token_secret']

    # Store oauth_token and oauth_token_secret so they can be used at the next stage of the sign in process.
    async with request.app['db_engine'].acquire() as conn:
        result = await conn.execute(login_sessions_table.select().where(login_sessions_table.c.oauth_token == oauth_token))
        login_session = await result.first()
        if login_session is None:
            async with transaction_context(conn) as tc_conn:
                await tc_conn.execute(login_sessions_table.insert().values(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret))

    raise web.HTTPFound(URL(authenticate_endpoint) % {'oauth_token': oauth_token})


async def token(request):
    params = request.query
    params_oauth_token = params.get('oauth_token')
    oauth_verifier = params.get('oauth_verifier')
    oauth_token = None
    oauth_token_secret = None

    async with request.app['db_engine'].acquire() as conn:
        result = await conn.execute(login_sessions_table.select().where(login_sessions_table.c.oauth_token == params_oauth_token))
        session_data = await result.first()
        if session_data is None:
            raise web.HTTPBadRequest('Could not verify the OAuth token')
        session_data = {column: value for column, value in session_data.items()}
        oauth_token = session_data['oauth_token']
        oauth_token_secret = session_data['oauth_token_secret']
        # Clean up login session data. This should also be done periodically for example using a background task.
        # https://docs.aiohttp.org/en/stable/web_advanced.html#background-tasks
        await conn.execute(login_sessions_table.delete().where(login_sessions_table.c.oauth_token == params_oauth_token))

    if oauth_token != params_oauth_token:
        raise web.HTTPBadRequest('Could not verify the Oauth token')

    twitter_api_key = request.app['twitter_api_key']
    twitter_api_secret_key = request.app['twitter_api_secret_key']
    access_token_endpoint = request.app['access_token_endpoint']

    client = oauthlib.oauth1.Client(twitter_api_key, client_secret=twitter_api_secret_key,
                                    resource_owner_key=oauth_token, resource_owner_secret=oauth_token_secret)
    request_body = f'oauth_verifier={oauth_verifier}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    uri, headers, request_body = client.sign(access_token_endpoint, http_method='POST', headers=headers, body=request_body)

    session = request.app['client_session']

    async with session.post(uri, headers=headers, data=request_body) as response:
        if response.status != 200:
            raise web.HTTPInternalServerError('Could not receive an access token')
        body = await response.text()

    # Parse oauth_token, oauth_token_secret, user_id, screen_name.
    body = dict([pair.split('=') for pair in body.split('&')])
    user_id_third_step = body['user_id']

    # Determine identity of the user using GET account/verify_credentials.
    client = oauthlib.oauth1.Client(twitter_api_key, client_secret=twitter_api_secret_key,
                                    resource_owner_key=body['oauth_token'], resource_owner_secret=body['oauth_token_secret'])
    verify_credentials_endpoint = request.app['verify_credentials_endpoint']
    uri, headers, _ = client.sign(verify_credentials_endpoint, http_method='GET')

    async with session.get(uri, headers=headers) as response:
        if response.status != 200:
            raise web.HTTPInternalServerError('Could not verify user identity')
        body = await response.json()

    user_id = body['id_str']
    user_screen_name = body['screen_name']

    if user_id != user_id_third_step:
        raise web.HTTPInternalServerError('User identity mismatch')

    # Store user data in the database if it is not already present.
    async with request.app['db_engine'].acquire() as conn:
            result = await conn.execute(users_table.select().where(users_table.c.user_id == user_id))
            user = await result.first()
            if user is None:
                async with transaction_context(conn) as tc_conn:
                    await tc_conn.execute(users_table.insert().values(user_id=user_id, screen_name=user_screen_name))

    # Issue a JWT for the user. 
    encoded = _create_token(user_id, user_screen_name, request.app['jwt_key'], request.app['jwt_algorithm']) 

    response = web.HTTPFound('/')
    response.set_cookie(TOKEN_COOKIE, encoded, max_age=60*60*24, secure=True, samesite='Strict', httponly=True)  # Should expire in 24h.
    response.set_cookie('screenName', user_screen_name, max_age=60*60*24, secure=True, samesite='Strict')

    return response


async def invalidate_token(request):
    response = web.HTTPNoContent()
    response.del_cookie(TOKEN_COOKIE)
    return response


async def jane_login(request):
    encoded = _create_token(jane['user_id'], jane['screen_name'], request.app['jwt_key'], request.app['jwt_algorithm'])

    response = web.HTTPFound('/')
    response.set_cookie(TOKEN_COOKIE, encoded, max_age=60*60*24, secure=True, samesite='Strict', httponly=True)  # Should expire in 24h.
    response.set_cookie('screenName', jane['screen_name'], max_age=60*60*24, secure=True, samesite='Strict')

    return response


async def john_login(request):
    encoded = _create_token(john['user_id'], john['screen_name'], request.app['jwt_key'], request.app['jwt_algorithm'])

    response = web.HTTPFound('/')
    response.set_cookie(TOKEN_COOKIE, encoded, max_age=60*60*24, secure=True, samesite='Strict', httponly=True)  # Should expire in 24h.
    response.set_cookie('screenName', john['screen_name'], max_age=60*60*24, secure=True, samesite='Strict')

    return response
