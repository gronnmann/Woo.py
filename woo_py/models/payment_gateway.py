from enum import Enum
from pydantic import BaseModel


class PaymentGatewayType(str, Enum):
    text = "text"
    email = "email"
    number = "number"
    color = "color"
    password = "password"
    textarea = "textarea"
    select = "select"
    multiselect = "multiselect"
    radio = "radio"
    image_width = "image_width"
    checkbox = "checkbox"

class PaymentGatewaySetting(BaseModel):
    id: str
    label: str
    description: str | None = None
    type: PaymentGatewayType | None = None
    value: str | None = None
    default: str | None = None
    tip: str | None = None
    placeholder: str | None = None
    options: dict[str, str] | None = None


class PaymentGateway(BaseModel):
    id: str
    title: str
    description: str | None = None
    order: int | None = None
    enabled: bool = False
    method_title: str | None = None
    method_description: str | None = None
    method_supports: list[str] = []
    settings: dict[str, PaymentGatewaySetting] | None = None