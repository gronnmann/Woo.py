from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class SettingOption(BaseModel):
    id: str
    label: str
    description: str | None = None
    value: str | Dict[str, Any] | List[Any] | None = None
    default: str | Dict[str, Any] | List[Any] | None = None
    tip: str | None = None
    placeholder: str | None = None
    type: str
    options: Dict[str, str] | None = None
    group_id: str | None = None