from datetime import datetime, date


class DayData:
    def __init__(self, dt: date) -> None:
        self._dt = dt
        self.name = dt.strftime("%d %B %Y")
        self.url = dt.strftime("%d_%m_%Y")

        self.selected = False

    def date(self):
        return self._dt

    @property
    def is_weekday(self):
        return self._dt.weekday() in [5, 6]

    @property
    def day_month(self):
        return self._dt.strftime("%d %B")

class User:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name


class CalendarDay:
    def __init__(self, dt: datetime):
        self._dt = dt

    @property
    def weekday(self):
        return 1