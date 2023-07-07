from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Station(BaseModel):
    name: str
    place: str
    id: str
    divaId: int
    abbreviation: str
    tariffZones: str
    products: List[str]
    latitude: float
    longitude: float
