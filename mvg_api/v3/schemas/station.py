from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Station(BaseModel):
    """Information about a station"""
    name: str
    """Name of the station"""
    place: str
    """General place of the station"""
    id: str
    """IFOPT global id of the station"""
    divaId: int
    """Diva id of the station, typically station identifier of IFOPT id"""
    abbreviation: str
    """MVG id of the station"""
    tariffZones: str
    """Tariff zones assigned to the station; either a single zone (e.g. 'm' or '2') or two neighboring zones (e.g. 'm|1' or '4|5'); only set on type STATION"""
    products: List[str]
    """transport types servicing this location; only set on type STATION"""
    latitude: float
    """The latitude of the location"""
    longitude: float
    """The longitude of the location"""
