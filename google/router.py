from fastapi import APIRouter
from . import authorize

router = APIRouter()

router.include_router(authorize.router)
