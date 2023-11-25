import routers
from fastapi import FastAPI

app = FastAPI()

for router in routers.all_router:
    app.include_router(router)
