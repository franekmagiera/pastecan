from pastecan.handlers import (
    delete_paste,
    get_index,
    get_paste,
    get_pastes,
    invalidate_token,
    jane_login,
    john_login,
    post_paste,
    put_paste,
    token,
    twitter_login
)
from pastecan.settings import STATIC_DIR

def setup_routes(app):
    # Catch all routes used on the front end and return the index page.
    # Routing is handled on the client side by preact-router.
    # In production environment it would be better to confugre a reverse proxy for this purpose.
    app.router.add_get('/', get_index)
    app.router.add_get('/archive', get_index)
    app.router.add_get(r'/pastes/{id:\d+}', get_index)
    app.router.add_get(r'/users/{name:.+}', get_index)


    # API endpoints.
    app.router.add_delete('/api/pastes/{id}', delete_paste)
    app.router.add_get('/api/pastes', get_pastes)
    app.router.add_get('/api/pastes/{id}', get_paste)
    app.router.add_post('/api/pastes', post_paste)
    app.router.add_put('/api/pastes/{id}', put_paste)
    app.router.add_get('/api/token', token)
    app.router.add_get('/api/twitter_login', twitter_login)
    app.router.add_get('/api/logout', invalidate_token)

    # Endpoints for logging in as mock users for demonstration purposes.
    app.router.add_get('/api/jane_login', jane_login)
    app.router.add_get('/api/john_login', john_login)

    app.router.add_static('/', path=STATIC_DIR)
