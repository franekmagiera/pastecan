# Pastecan
![pastecan-print-screen](/docs/static/pastecan.png)

Pastecan is a [pastebin](https://pastebin.com/) clone. The backend is powered by a MySQL database and a REST API built with Python using the [aiohttp](https://docs.aiohttp.org/en/stable/) framework. The client side is a Single Page Application (SPA) created with TypeScript using preact, preact-router, react-bootstrap. (For a complete list of packages used see `package.json` and `requirements.txt`)

## Features
  * CRUD operations on pastes
    * Guests can create and browse public pastes
    * Logged in users can CRUD their public and private pastes
  * Log in with Twitter
  * Syntax highlighting

## Design
 * Paste and user data is stored in a relational database (MySQL).
 * The API is mostly RESTful - session data is only stored for short periods of time for the purposes of Log In with Twitter's 3-legged OAuth process described [here](https://developer.twitter.com/en/docs/authentication/guides/log-in-with-twitter). API is implemented with an event loop (python asyncio, aiohttp).
 * After successfuly authenticating the user with Twitter, a JWT is issued that can be used for authorization for future requests.
 * The JWT is stored as a cookie and is sent with `Secure, SameSite: Strict` and `httpOnly` options.
 * The front end is an SPA based on preact and preact-router.
 * In order for relative URLs to work a "Catch all" approach is implemented on the server side. This issue is nicely described [here](https://stackoverflow.com/a/36623117). For development purposes and simplicity this is done using aiohttp, in production environment it would be better to configure a reverse proxy for this purpose.
 * In production environment it is crucial to set up HTTPS as well.

## How to run?
Requirements:
- Nodejs 22.15.1
- Python 3.12.1

Example configuration is presented in `config/example_config.yaml`. This file should be renamed to `config.yaml` after applying suitable changes (for example after changing JWT key and Twitter API keys). Files containing confidential information should be included in a `.gitignore` file.

To run:

```
$ cd pastecan

$ yarn install
$ yarn build

$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt

$ docker-compose up -d

$ python main.py
```

## TODO:
 * Handle cases where user denies access via Twitter
 * Add tests, `flake8`, `black`, `mypy`
 * Add input sanitization on the client side
 * Create swagger documentation
 * Enable type checks on error catches in UI code
 * Verify HS256 vs RS256 (or any other method)
