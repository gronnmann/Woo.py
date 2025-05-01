from enum import Enum
from typing import Any, Dict, List, Literal, Union
from pydantic import BaseModel, Field


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
    # Make type more flexible to handle various input values
    type: str | None = None
    # Allow value to be string, list, or dict to accommodate different setting types
    value: Union[str, List[str], Dict[str, Any], None] = None
    # Allow default to be string, list, or dict
    default: Union[str, List[str], Dict[str, Any], None] = None
    tip: str | None = None
    placeholder: str | None = None
    options: Dict[str, str | dict[str, Any]] | None = None


class PaymentGateway(BaseModel):
    id: str
    title: str | None = None  # Make title optional since it can be None in responses
    description: str | None = None
    order: int | Literal[""] | None = None  # No sort order -> gives ''
    enabled: bool = False
    method_title: str | None = None
    method_description: str | None = None
    method_supports: List[str] = []
    settings: list[PaymentGatewaySetting] | Dict[str, PaymentGatewaySetting] | None = (
        None
    )
