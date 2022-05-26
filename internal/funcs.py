from datetime import timedelta
from typing import List
from internal.classes import *
from calendar import Calendar

import aiofiles

import json


def get_show_days(show_date: str) -> List[DayData]:
    delta = timedelta(days=1)
    today = datetime.strptime(show_date, '%d_%m_%Y').date()

    tomorrow = today + delta
    yesterday = today - delta

    i = 1
    while tomorrow.weekday() in [5, 6]:
        tomorrow = today + timedelta(days=i)
        i += 1

    i = 1
    while yesterday.weekday() in [5, 6]:
        yesterday = today - timedelta(days=i)
        i += 1

    res_list = [
        DayData(yesterday),
        DayData(today),
        DayData(tomorrow),
    ]

    return res_list


async def get_remote_worker(day: DayData) -> List[User]:
    async with aiofiles.open("remote_data/remote_work_data.json", mode="r", encoding="utf-8") as read:
        data_list = await read.read()
    data_list = json.loads(data_list)

    res = []
    for (m, dt) in data_list:
        check_data = datetime.strptime(dt, '%d.%m.%Y').date()
        if check_data == day.date():
            u = await get_user(int(m))
            res.append(u)
    return list(set(res))


async def get_user(user_id: int):
    async with aiofiles.open("remote_data/users.json", mode="r", encoding="utf-8") as read:
        data = await read.read()
    data = json.loads(data)

    name_user = data.get(str(user_id))
    return User(user_id, name_user)


async def get_days_by_user(user: User) -> List[DayData]:
    async with aiofiles.open("remote_data/remote_work_data.json", mode="r", encoding="utf-8") as read:
        data_list = await read.read()
    data_list = json.loads(data_list)

    res = []
    for (m, dt) in data_list:
        if str(m) == str(user.id):
            res.append(DayData(datetime.strptime(dt, '%d.%m.%Y')))
    return res


def get_calendar(month: int, year: int, selected_day_list: List[DayData]) -> List[List[DayData]]:
    c = Calendar()
    r = []
    week = []
    for id_x, x in enumerate(c.itermonthdates(year=year, month=month)):
        inst_day_data = DayData(datetime(year=x.year, month=x.month, day=x.day))
        week.append(inst_day_data)
        for d in selected_day_list:
            if d.date() == inst_day_data.date():
                inst_day_data.selected = True
        if id_x % 7 == 6:
            r.append(week)
            week = []
    return r
