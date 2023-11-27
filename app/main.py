import routers

from dotenv import load_dotenv
from fastapi import FastAPI


class BaseFastAPI(FastAPI):
    def setup(self) -> None:
        load_dotenv()

        super().setup()


app = BaseFastAPI()

for router in routers.all_router:
    app.include_router(router)
