from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Station(BaseModel):
    latitude: float
    longitude: float
    place: str
    name: str
    globalId: str
    divaId: int
    hasZoomData: bool
    transportTypes: List[str]
    surroundingPlanLink: str
    aliases: str
    tariffZones: str


class Locations(BaseModel):
    hash: str
    stations: List[Station]
