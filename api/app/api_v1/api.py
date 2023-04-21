from api_v1.routes import health, ingest
from fastapi import APIRouter

router = APIRouter()

router.include_router(health.router)
router.include_router(ingest.router)
