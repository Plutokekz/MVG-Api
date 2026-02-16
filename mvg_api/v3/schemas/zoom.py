from __future__ import annotations

from enum import Enum
from typing import List, Optional,  Union

from pydantic import BaseModel, field_validator

from mvg_api.v3.schemas import create_flexible_enum_validator


class PlannedMaintenance(BaseModel):
    status: TransportDeviceStatus
    """unkown: only encountered 'AUSSER_BETRIEB'"""
    since: int
    """Begin of the maintenance window as millisecond timestamp"""
    until: int
    """End of the maintenance window as millisecond timestamp"""
    description: str
    """Nicetext reason of the maintenance (e.g. Baustelle, Erneuerung)"""


class TransportDeviceStatus(Enum):
    """Status of the device. Note that planned is not a status, but may be derived from the planned information."""
    IN_BETRIEB = "IN_BETRIEB"
    WARTUNG = "WARTUNG"
    AUSSER_BETRIEB = "AUSSER_BETRIEB"
    UNBEKANNT = "UNBEKANNT"


class TransportDeviceType(Enum):
    FAHRSTUHL = "FAHRSTUHL"
    ROLLTREPPE = "ROLLTREPPE"


class TransportDevice(BaseModel):
    """
    One single escalator or elevator in a station.
    The coordinates refer to the zoom maps available on
    https://www.mvg.de/.rest/mvgZoom/api/stations/$efaId/map
    """
    description: str
    """Nicetext description of the location"""
    identifier: str
    """Identifier of the device in the mvg network (e.g. SE01 for Sendlinger Tor device 1)"""
    lastUpdate: Optional[int]
    """Presumably when the last status update was received from the device as millisecond timestamp"""
    name: str
    """Name of the device; identical to the identifier"""
    status: Union[TransportDeviceStatus, str]
    """Status of the device"""
    type: Union[TransportDeviceType, str]
    """Type of the transport device"""
    xcoordinate: int
    """X coordinate of the device on the zoom plan"""
    ycoordinate: int
    """Y coordinate of the device on the zoom plan"""
    planned:  Optional[PlannedMaintenance]
    """Information about planned maintenance"""

    # flexible validators such that pydantic does not fail if a value that is not in the enum is encountered
    _validate_status = field_validator('status', mode='before')(create_flexible_enum_validator(TransportDeviceStatus))
    _validate_type = field_validator('type', mode='before')(create_flexible_enum_validator(TransportDeviceType))


class ZoomStation(BaseModel):
    """Contains all zoom information about a station"""
    efaId: int
    """The divaId/efaId of the station"""
    name: str
    """Name of the station"""
    transportDevices: List[TransportDevice]
    """All transport devices (escalators and elevators) in this station and their properties"""
    aggregatedStatusROLLTREPPE: Union[TransportDeviceStatus, str]
    """Aggregated status of escalators: 'AUSSER_BETRIEB' as soon as one is not operational."""
    aggregatedStatusFAHRSTUHL: Union[TransportDeviceStatus, str]
    """Aggregated status of elevators: 'AUSSER_BETRIEB' as soon as one is not operational."""

    _validate_aggregatedStatusROLLTREPPE = field_validator('aggregatedStatusROLLTREPPE', mode='before')(create_flexible_enum_validator(TransportDeviceStatus))
    _validate_aggregatedStatusFAHRSTUHL = field_validator('aggregatedStatusFAHRSTUHL', mode='before')(create_flexible_enum_validator(TransportDeviceStatus))
