from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Aushang(BaseModel):
    uri: str
    scheduleKind: str
    scheduleName: str
    direction: str


class Aushaenge(BaseModel):
    __root__: List[Aushang]
