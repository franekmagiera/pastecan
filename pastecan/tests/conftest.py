import pytest
from testcontainers.mysql import MySqlContainer
from yaml import safe_load

from pastecan.settings import CONFIG_DIR

with open(CONFIG_DIR / 'test_config.yaml', 'r') as file:
    TEST_CONFIG = safe_load(file)

@pytest.fixture(scope="session")
async def mysql_container():
    port = int(TEST_CONFIG['MYSQL_PORT'])
    with MySqlContainer(
            "mysql:9.3",
            user=TEST_CONFIG['MYSQL_USER'],
            dbname=TEST_CONFIG['MYSQL_DB'],
            root_password=TEST_CONFIG['MYSQL_PASSWORD'],
            password=TEST_CONFIG['MYSQL_PASSWORD'],
            port=port
            ) as mysql_container:
        yield mysql_container

