from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, field_validator

from mvg_api.v3.schemas import create_flexible_enum_validator, StationTransportType, TariffZones


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
    abbreviation: Optional[str] = None
    """MVG id of the station"""
    tariffZones: str
    """Tariff zones assigned to the station"""
    products: List[StationTransportType]
    """transport types servicing this location; only set on type STATION"""
    latitude: float
    """The latitude of the location"""
    longitude: float
    """The longitude of the location"""

    _validate_products = field_validator('products', mode='before')(
        create_flexible_enum_validator(StationTransportType, is_list=True))

    def tariff_zones_common(self) -> TariffZones:
        """Obtain common representation of tariffZones."""
        return TariffZones(self.tariffZones)
