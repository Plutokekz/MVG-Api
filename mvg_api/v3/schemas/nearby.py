from __future__ import annotations

from typing import List
from pydantic import BaseModel, RootModel, field_validator

from mvg_api.v3.schemas import (
    create_flexible_enum_validator,
    StationTransportType,
    TariffZones,
)


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
    transportTypes: List[StationTransportType]
    """transport types servicing this location; only set on type STATION"""
    tariffZones: str
    """Tariff zones assigned to the station; either a single zone (e.g. 'm' or '2') or
    two neighboring zones (e.g. 'm|1' or '4|5'); only set on type STATION"""
    aliases: str
    """alternative names of the station, presumably to facilitate search optimization"""
    divaId: int
    """Diva id of the station, typically station identifier of IFOPT id"""
    hasZoomData: bool
    """Whether there is zoom data (escalator/elevator status) available for this station"""
    distanceInMeters: int
    """Linear distance to the station in meters"""

    _validate_transportTypes = field_validator("transportTypes", mode="before")(
        create_flexible_enum_validator(StationTransportType, is_list=True)
    )

    def tariff_zones_common(self) -> TariffZones:
        """Obtain common representation of tariffZones."""
        return TariffZones(self.tariffZones)


class Stations(RootModel):
    """A list of nearby stations with the respective linear distance"""

    root: List[Station]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
