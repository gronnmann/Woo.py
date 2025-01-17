from pydantic import BaseModel
from pydantic_changedetect import ChangeDetectionMixin


class TaxClass(ChangeDetectionMixin, BaseModel):
    slug: str | None = None
    name: str
