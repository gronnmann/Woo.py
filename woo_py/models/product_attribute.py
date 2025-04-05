from enum import Enum
from pydantic import BaseModel
from pydantic_changedetect import ChangeDetectionMixin


class AttributeOrderBy(str, Enum):
    NAME = "name"
    NAME_NUM = "name_num"
    ID = "id"
    MENU_ORDER = "menu_order"


class AttributeType(str, Enum):
    SELECT = "select"


class ProductAttribute(ChangeDetectionMixin, BaseModel):
    id: int | None = None
    name: str
    slug: str | None = None
    type: AttributeType | str = AttributeType.SELECT
    order_by: AttributeOrderBy = AttributeOrderBy.MENU_ORDER
    has_archives: bool = False
    terms: list[str] | None = None