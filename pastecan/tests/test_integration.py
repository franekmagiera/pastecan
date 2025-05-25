import pytest
from aiohttp import test_utils
from aiomysql.sa import create_engine
from contextlib import asynccontextmanager

from pastecan.app import init_app
from .conftest import TEST_CONFIG

@pytest.mark.asyncio
async def test_create_and_get_paste(mysql_container):
    async with create_test_app(mysql_container) as test_app:
        server = test_utils.TestServer(test_app)
        client = test_utils.TestClient(server)
        await client.start_server()

        paste_content = "square = lambda x: x * x"
        paste_data = {
            "language": "python",
            "content": paste_content,
            "title": "Square",
            "exposure": "Public"
        }

        # Create a new paste as guest (without authentication).
        resp = await client.post("/api/pastes", json=paste_data)
        assert resp.status == 200, f"Expected status 200, got {resp.status}"
        data = await resp.json()
        paste_id = data.get("id")
        assert paste_id is not None, "Paste ID should be returned after creation."

        # Get the newly created paste.
        resp = await client.get(f"/api/pastes/{paste_id}")
        assert resp.status == 200, f"Expected status 200, got {resp.status}"
        data = await resp.json()

        # Assert that the paste content is the same as what was created.
        assert data.get("content") == paste_content, "Paste content does not match the created content."


@asynccontextmanager
async def create_test_app(mysql_container):
    exposed_port = int(mysql_container.get_exposed_port(TEST_CONFIG["MYSQL_PORT"]))
    test_db_engine = await create_db_engine(exposed_port)
    test_app = await init_app(TEST_CONFIG, test_db_engine)
    try:
        yield test_app
    finally:
        await test_app.shutdown()
        await test_app.cleanup()


async def create_db_engine(exposed_port):
    return await create_engine(
            user=TEST_CONFIG['MYSQL_USER'],
            db=TEST_CONFIG['MYSQL_DB'],
            host=TEST_CONFIG['MYSQL_HOST'],
            password=TEST_CONFIG['MYSQL_PASSWORD'],
            port=exposed_port
            )

