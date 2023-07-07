from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Line(BaseModel):
    label: str
    transportType: str
    network: str
    divaId: str
    sev: bool


class Lines(BaseModel):
    __root__: List[Line]
