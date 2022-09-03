from aerich import Command
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from rearq.server.app import app as rearq_server
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from brew.exceptions import (
    custom_http_exception_handler,
    not_exists_exception_handler,
    validation_exception_handler,
    exception_handler,
)
from brew.logging import init_logging
from brew.routers import router
from brew.settings import settings, TORTOISE_ORM
from brew.tasks import rearq

if settings.DEBUG:
    app = FastAPI(title="brew", description="Search for brew", debug=settings.DEBUG)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
else:
    app = FastAPI(
        title="brew",
        description="Search for brew",
        debug=settings.DEBUG,
        redoc_url=None,
        docs_url=None,
    )
app.include_router(router)
register_tortoise(
    app,
    config=TORTOISE_ORM,
)
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(DoesNotExist, not_exists_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, exception_handler)
app.mount("/rearq", rearq_server)
rearq_server.set_rearq(rearq)


@app.on_event("startup")
async def startup():
    await rearq.init()
    init_logging()
    aerich = Command(TORTOISE_ORM)
    await aerich.init()
    await aerich.upgrade()


@app.on_event("shutdown")
async def shutdown():
    await rearq.close()
