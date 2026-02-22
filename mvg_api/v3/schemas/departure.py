from __future__ import annotations

from typing import List, Optional
from pydantic import field_validator, BaseModel, RootModel

from mvg_api.v3.network import NetworkLine
from mvg_api.v3.schemas import create_flexible_enum_validator, MessageType, Occupancy


class Info(BaseModel):
    """
    Information regarding a service in the departure board
    Examples for encountered messages:
    {'message': 'Verspätung aus vorheriger Fahrt', 'type': 'INCIDENT', 'network': 'ddb'}
    {'message': 'Reparatur an einem Signal', 'type': 'INCIDENT', 'network': 'ddb'}
    """
    message: str
    """The message text"""
    type: MessageType
    """Type of the message: only encountered 'INCIDENT'"""
    network: str
    """unknown: provider of the message"""

    _validate_type = field_validator('type', mode='before')(create_flexible_enum_validator(MessageType))


class Departure(BaseModel):
    """A departure of a planned service at a station"""
    plannedDepartureTime: int
    """The planned departure time as millisecond timestamp (minute precision)"""
    realtime: bool
    """Whether there is real time information about the departure time"""
    delayInMinutes: Optional[int] = 0
    """Expected delay of the departure in minutes"""
    realtimeDepartureTime: int
    """Real time departure as millisecond timestamp (second precision)"""
    transportType: str
    """Transport type of this service"""
    label: str
    """The line label, e.g. U4"""
    divaId: str
    """unknown"""
    network: str
    """provider; encountered 'ddb' for Deutsche Bahn, 'swm' for ubahn, 'mvv' for buses, 'unknown' for fussweg"""
    trainType: str
    """unknown: empty string?"""
    destination: str
    """Name of the destination station"""
    cancelled: bool
    """Whether this service was cancelled"""
    sev: bool
    """unknown: presumably that this service is replaced by SEV or _is_ SEV and replacing a service"""
    platform: Optional[int] = None
    """Platform number, typically only with train, sbahn and ubahn services"""
    platformChanged: Optional[bool] = None
    """Whether the platform has changed"""
    stopPositionNumber: Optional[int] = None
    """Stop (Haltestelle) position, typically only with tram and bus services"""
    messages: List
    """unknown: empty"""
    infos: List[Info]
    """Information regarding this particular service"""
    bannerHash: str
    """unknown: empty"""
    occupancy: Occupancy
    """Expected occupancy of this service"""
    stationGlobalId: Optional[str] = None
    """IFOPT global id of the station"""
    stopPointGlobalId: Optional[str] = None
    """IFOPT global id of the stop point"""
    lineId: Optional[str] = None
    """Id of this particular service line, presumably matching GTFS data"""
    tripId: Optional[str] = None
    """unknown: only set very rarely, primarily encountered on night lines; does not change over days"""
    tripCode: Optional[int] = None
    """unknown: presumably identifying this particular service and line on a day (does not change over days)"""

    _validate_occupancy = field_validator('occupancy', mode='before')(create_flexible_enum_validator(Occupancy))

    def to_network_line(self):
        """Converts this line descriptor to the standardized network line"""
        return NetworkLine.of_any(self)


class Departures(RootModel):
    """A list of departures of a station as returned by the API."""
    root: List[Departure]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
