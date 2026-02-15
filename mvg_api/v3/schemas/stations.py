from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Station(BaseModel):
    """Information about a station"""
    globalId: str
    """IFOPT global id of the station"""
    name: str
    """Name of the station"""
    place: str
    """General place of the station"""
    latitude: float
    """The latitude of the location"""
    longitude: float
    """The longitude of the location"""
    transportTypes: List[str]
    """transport types servicing this location; only set on type STATION"""
    tariffZones: str
    """Tariff zones assigned to the station; either a single zone (e.g. 'm' or '2') or two neighboring zones (e.g. 'm|1' or '4|5'); only set on type STATION"""
    aliases: str
    """alternative names of the station, presumably to facilitate search optimization"""
    divaId: int
    """Diva id of the station, typically station identifier of IFOPT id"""
    hasZoomData: bool
    """Whether there is zoom data (escalator/elevator status) available for this station"""

class Stations(BaseModel):
    """A list of MVV stations as returns by the API"""
    hash: str
    """A hash, presumably to identify the result, that can be resubmitted when querying new data to avoid unnecessary exchanges if nothing changed."""
    stations: List[Station]
    """The actual stations list."""
