from aiohttp import web
from aiomysql.sa import create_engine
import asyncio
from yaml import safe_load
from pastecan.app import init_app
from pastecan.db import create_tables, insert_mock_data
from pastecan.settings import CONFIG_DIR


def main():
    with open(CONFIG_DIR / 'config.yaml', 'r') as file:
        config = safe_load(file)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    db_engine = loop.run_until_complete(
        create_engine(
            user=config['MYSQL_USER'],
            db=config['MYSQL_DB'],
            host=config['MYSQL_HOST'],
            password=config['MYSQL_PASSWORD'],
            port=config['MYSQL_PORT']
        ))
    loop.run_until_complete(create_tables(db_engine))
    loop.run_until_complete(insert_mock_data(db_engine))

    app = loop.run_until_complete(init_app(config, db_engine))
    web.run_app(app, loop=loop)


if __name__ == '__main__':
    main()

