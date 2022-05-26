from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from internal.funcs import *

templates = Jinja2Templates(directory="templates")

date_api_router = APIRouter()


@date_api_router.get("/{show_date}", response_class=HTMLResponse)
async def read_item(request: Request, show_date: str):
    yesterday, today, tomorrow, = get_show_days(show_date)

    param = {
        "request": request,
        "today": today,
        "tomorrow": tomorrow,
        "yesterday": yesterday,
        "today_members": await get_remote_worker(today),
        "tomorrow_members": await get_remote_worker(tomorrow),
        "yesterday_members": await get_remote_worker(yesterday),
    }

    return templates.TemplateResponse("index.html", param)