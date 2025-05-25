from aiohttp import ClientSession, web

from pastecan.db import create_tables
from pastecan.routes import setup_routes


async def on_shutdown(app):
    await app['client_session'].close()
    app['db_engine'].close()
    await app['db_engine'].wait_closed()


# TODO: move this out of main.py.
async def init_app(config, db_engine):
    app = web.Application()

    app['db_engine'] = db_engine
    await create_tables(db_engine)

    app['request_token_endpoint'] = config['REQUEST_TOKEN_ENDPOINT']
    app['authenticate_endpoint'] = config['AUTHENTICATE_ENDPOINT']
    app['access_token_endpoint'] = config['ACCESS_TOKEN_ENDPOINT']
    app['verify_credentials_endpoint'] = config['VERIFY_CREDENTIALS_ENDPOINT']
    app['twitter_api_key'] = config['TWITTER_API_KEY']
    app['twitter_api_secret_key'] = config['TWITTER_API_SECRET_KEY']
    app['twitter_oauth_callback'] = config['OAUTH_CALLBACK']
    
    app['jwt_key'] = config['JWT_KEY']
    app['jwt_algorithm'] = config['JWT_ALGORITHM']

    app['client_session'] = ClientSession()

    app.on_shutdown.append(on_shutdown)

    setup_routes(app)

    return app
