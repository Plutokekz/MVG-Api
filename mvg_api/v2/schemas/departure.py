from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Departure(BaseModel):
    plannedDepartureTime: int
    realtime: bool
    delayInMinutes: Optional[int] = None
    realtimeDepartureTime: int
    transportType: str
    label: str
    network: str
    trainType: str
    destination: str
    cancelled: bool
    sev: bool
    platform: Optional[int] = None
    messages: List
    bannerHash: str
    occupancy: str
    stopPointGlobalId: str


class Departures(BaseModel):
    __root__: List[Departure]
