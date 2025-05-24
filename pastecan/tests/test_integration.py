import asyncio
import pytest
from aiohttp import test_utils
from pastecan.main import init

@pytest.mark.asyncio
async def test_create_and_get_paste():
    app = await init(asyncio.get_running_loop())
    server = test_utils.TestServer(app)
    client = test_utils.TestClient(server)
    await client.start_server()

    paste_content = "Test Paste Content"
    paste_data = {
        "language": "python",
        "content": paste_content,
        "title": "Test Paste",
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

    await client.close()
    app['db_engine'].close()
    await app['db_engine'].wait_closed()

