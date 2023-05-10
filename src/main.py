import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import uvicorn
from fastapi import FastAPI

from src.app import routers
from src.config.settings import settings

import logging
from src.config.logger import configure_logging
configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION)

app.include_router(routers.api_router, prefix=settings.API_PREFIX)

if __name__ == '__main__':
    uvicorn.run("src.main:app", host='0.0.0.0',
                port=settings.SERVER_PORT,
                workers=settings.SERVER_WORKER_NUMBER,
                proxy_headers=True,
                forwarded_allow_ips='*',
                reload=settings.ENABLE_WEB_SERVER_AUTORELOAD)

