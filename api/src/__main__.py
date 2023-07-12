from aiohttp import web

from src.database.base import SessionFactory
from src.config import load_config

from src.views.router import Router

if __name__ == "__main__":
    config = load_config()
    SessionFactory.configure(config.postgres_dsn)
    app = web.Application()
    Router.setup_routes(app)

    web.run_app(app, port=config.api_port)
