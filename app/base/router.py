from fastapi import APIRouter


class BaseAPIRouter(APIRouter):
    response = {404: {"description": "Not found!"}}
