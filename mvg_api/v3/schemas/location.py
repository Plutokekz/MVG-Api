from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, RootModel, field_validator

from mvg_api.v3.schemas import create_flexible_enum_validator, OfferedTransportType, TariffZones


class LocationType(str, Enum):
    STATION = "STATION"
    ADDRESS = "ADDRESS"
    POI = "POI"


class Location(BaseModel):
    """A location representing a station, address or poi"""
    latitude: float
    """The latitude of the location"""
    longitude: float
    """The longitude of the location"""
    place: str
    """General place of the location"""
    name: str
    """Name of the location"""
    globalId: Optional[str] = None
    """IFOPT global id of the station; only set on type STATION"""
    divaId: Optional[int] = None
    """Diva id of the station, typically station identifier of IFOPT id; only set on type STATION"""
    hasZoomData: Optional[bool] = None
    """whether there is zoom data available for this station"""
    transportTypes: Optional[List[Union[OfferedTransportType, str]]] = None
    """transport types servicing this location; only set on type STATION"""
    aliases: Optional[str] = None
    """unknown: empty; previously alternative names of the location, presumably to facilitate search optimization"""
    tariffZones: Optional[str] = None
    """Tariff zones assigned to the station; either a single zone (e.g. 'm' or '2') or two neighboring zones (e.g. 'm|1' or '4|5'); only set on type STATION"""
    postCode: Optional[str] = None
    """Post code of the location; only set on type ADDRESS"""
    street: Optional[str] = None
    """Street name of the location; only set on type ADDRESS"""
    houseNumber: Optional[str] = None
    """House number of the location; only set on type ADDRESS"""
    type: LocationType
    """Type of the location"""

    _validate_transportTypes = field_validator('transportTypes', mode='before')(
        create_flexible_enum_validator(OfferedTransportType, is_list=True))

    def tariffZones_common(self) -> TariffZones:
        """Obtain common representation of tariffZones."""
        return TariffZones(self.tariffZones)


class Locations(RootModel):
    """A list of locations as returned by the API."""
    root: List[Location]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
