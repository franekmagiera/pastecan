import pytest
from testcontainers.mysql import MySqlContainer

@pytest.fixture(scope="session")
def mysql_container():
    # TODO: Read that from test configuration and also do the same in init?
    with MySqlContainer(
            "mysql:9.3",
            user="root",
            root_password="secret",
            password="secret",
            dbname="pastcan") as mysql:
        yield mysql

