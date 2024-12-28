import datetime

from pydantic import BaseModel
from pydantic_changedetect import ChangeDetectionMixin


class OrderNote(ChangeDetectionMixin, BaseModel):
    id: int | None = None
    author: str | None = None
    date_created: datetime.datetime | None = None
    date_created_gmt: datetime.datetime | None = None
    note: str
    customer_note: bool = False
    added_by_user: bool = False
