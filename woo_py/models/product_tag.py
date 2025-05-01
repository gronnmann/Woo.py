from pydantic import BaseModel
from pydantic_changedetect import ChangeDetectionMixin


class ProductTag(ChangeDetectionMixin, BaseModel):
    id: int | None = None
    name: str
    slug: str | None = None
    description: str | None = None
    count: int | None = None
