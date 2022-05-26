from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime

from routers import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_api_router, prefix='/user')
app.include_router(date_api_router, prefix='/date')


@app.get("/")
async def index():
    now = datetime.now().strftime("%d_%m_%Y")
    return RedirectResponse(f"/date/{now}")
