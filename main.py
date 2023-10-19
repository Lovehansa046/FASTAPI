from fastapi import FastAPI

from routers.test_auth_router import router as _router
from routers.main_router import router as _router_main

app = FastAPI()




app.include_router(_router)
app.include_router(_router_main)