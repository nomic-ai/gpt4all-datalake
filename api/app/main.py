import os
import docs
from api_v1 import events
from api_v1.api import router as v1_router
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware

from api_v1.settings import settings

import logging
from fastapi.logger import logger as fastapi_logger
logger = logging.getLogger(__name__)

app = FastAPI(title='GPT4All Datalake API', description=docs.desc)

# add v1
app.include_router(v1_router, prefix='/v1')
app.add_event_handler('startup', events.startup_event_handler(app))
app.add_exception_handler(HTTPException, events.on_http_error)

@app.on_event("startup")
async def startup():
    # establish a database connection

    if settings.app_environment == "dev":
        if not os.path.exists(os.path.join(settings.root_filesystem_path, 'data')):
            os.mkdir(os.path.join(settings.root_filesystem_path, 'data'))


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down API")


# filter out health endpoint from logging
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return True


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    gunicorn_logger = logging.getLogger("gunicorn")

    root_logger = logging.getLogger()
    fastapi_logger.setLevel(gunicorn_logger.level)
    fastapi_logger.handlers = gunicorn_error_logger.handlers
    root_logger.setLevel(gunicorn_logger.level)

    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.handlers = gunicorn_error_logger.handlers
else:
    # https://github.com/tiangolo/fastapi/issues/2019
    LOG_FORMAT2 = "[%(asctime)s %(process)d:%(threadName)s] %(name)s - %(levelname)s - %(message)s | %(filename)s:%(lineno)d"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT2)


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Headers", "Content-Type",
                   'Authorization', "Access-Control-Allow-Origin", "Set-Cookie"],
)
