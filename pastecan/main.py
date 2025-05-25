import asyncio
from aiohttp import ClientSession, web
from yaml import safe_load

from pastecan.db import init_db
from pastecan.routes import setup_routes
from pastecan.settings import CONFIG_DIR


async def on_shutdown(app):
    await app['client_session'].close()


async def init_app(loop):
    with open(CONFIG_DIR / 'config.yaml', 'r') as file:
        config = safe_load(file)

    db_engine = await init_db(
        user=config['MYSQL_USER'],
        db=config['MYSQL_DB'],
        host=config['HOST'],
        password=config['MYSQL_PASSWORD'],
        loop=loop
    )

    app = web.Application()
    app['db_engine'] = db_engine

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


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = loop.run_until_complete(init_app(loop))
    web.run_app(app, loop=loop)


if __name__ == '__main__':
    main()
