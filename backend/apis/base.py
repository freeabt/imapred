from fastapi import APIRouter

from apis.version1 import route_general_pages
from apis.version1 import route_predict_ima


api_router = APIRouter()
api_router.include_router(route_general_pages.general_pages_router,prefix="",tags=["general_pages"])
api_router.include_router(route_predict_ima.predict_router,prefix="",tags=["predict_ima"])