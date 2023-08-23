from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, RootModel


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


class Departures(RootModel):
    root: List[Departure]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
