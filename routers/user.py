from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from internal.funcs import *

templates = Jinja2Templates(directory="templates")

user_api_router = APIRouter()


@user_api_router.get("/{user_id}/{month}/{year}", response_class=HTMLResponse)
async def user_list(request: Request, user_id: int, month: int, year: int):
    user = await get_user(user_id)
    if user.name is None:
        return RedirectResponse("/")
    else:
        calendar = get_calendar(month, year, await get_days_by_user(user))

        cur_date = datetime(year=year, month=month, day=15).date()
        delta = timedelta(days=30)

        prev_month = cur_date - delta
        next_month = cur_date + delta

        param = {
            "request": request,
            "user": user,
            "calendar": calendar,
            "prev_month": prev_month,
            "next_month": next_month,
        }
        return templates.TemplateResponse("user.html", param)
