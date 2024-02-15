import asyncio

import uvicorn
from fastapi import FastAPI
from loguru import logger

from spiders import spiders


def init_app():
    _app = FastAPI(title="0713")

    register_blueprints(_app)
    inject_app_on_startup(_app)

    return _app


def inject_app_on_startup(_app: FastAPI):
    @_app.on_event("startup")
    async def startup():
        # async spiders
        event_loop = asyncio.get_event_loop()
        for spider in spiders.values():
            event_loop.create_task(spider())
            logger.success(f"start crawler: {spider.NAME}")


def register_blueprints(_app):
    from app import routers
    _app.include_router(routers.router, prefix="/v1/api")


def run(host, port):
    _app = init_app()
    uvicorn.run(_app, port=port, host=host)
