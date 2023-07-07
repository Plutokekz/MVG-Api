from __future__ import annotations

from typing import List

from pydantic import BaseModel


class BasePlan(BaseModel):
    planId: str
    stationName: str
    fileSize: int
    md5Hash: str
    minLatitude: float
    maxLatitude: float
    minLongitude: float
    maxLongitude: float


class Plan(BasePlan):
    content: str


class Plans(BaseModel):
    __root__: List[BasePlan]
