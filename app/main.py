import routers

from dotenv import load_dotenv
from fastapi import FastAPI
from database.base import Base, engine


class BaseFastAPI(FastAPI):
    def setup(self) -> None:
        # setup environment variable
        load_dotenv()

        # setup database
        Base.metadata.create_all(bind=engine)

        super().setup()


app = BaseFastAPI()

for router in routers.all_router:
    app.include_router(router)
