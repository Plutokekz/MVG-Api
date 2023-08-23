from __future__ import annotations

from typing import List

from pydantic import BaseModel, RootModel


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


class Plans(RootModel):
    root: List[BasePlan]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
