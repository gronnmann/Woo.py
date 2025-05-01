from pydantic import BaseModel
from typing import Dict, List, Optional


class Country(BaseModel):
    code: str
    name: str
    states: List[Dict[str, str | int]] | None = None


class Currency(BaseModel):
    code: str
    name: str
    symbol: str
    position: str | None = None
    thousand_separator: str | None = None
    decimal_separator: str | None = None
    decimals: int | None = None
