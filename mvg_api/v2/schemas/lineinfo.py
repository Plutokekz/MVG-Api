from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Key(BaseModel):
    transportType: str
    label: Optional[str] = None


class Info(BaseModel):
    key: Key
    value: str


class Infos(BaseModel):
    __root__: List[Info]
