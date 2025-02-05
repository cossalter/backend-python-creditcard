from routers import all_router

from dotenv import load_dotenv
from fastapi import FastAPI
from database.base import BaseModel, engine


def on_startup():
    # setup environment variable
    load_dotenv()

    # setup database
    BaseModel.metadata.create_all(bind=engine)


app = FastAPI(on_startup=[on_startup])

for router in all_router:
    app.include_router(router)
