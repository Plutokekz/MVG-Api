from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class LocationType(str, Enum):
    STATION = "STATION"
    ADDRESS = "ADDRESS"
    POI = "POI"


class Location(BaseModel):
    type: LocationType
    latitude: float
    longitude: float
    place: str
    name: str
    globalId: Optional[str] = None
    divaId: Optional[int] = None
    hasZoomData: Optional[bool] = None
    transportTypes: Optional[List[str]] = None
    surroundingPlanLink: Optional[str] = None
    aliases: Optional[str] = None
    tariffZones: Optional[str] = None
    postCode: Optional[str] = None
    street: Optional[str] = None
    houseNumber: Optional[str] = None


class Locations(BaseModel):
    __root__: List[Location]
