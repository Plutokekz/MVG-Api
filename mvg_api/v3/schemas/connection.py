from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, RootModel


class Occupancy(str, Enum):
    UNKNOWN = "UNKNOWN"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Station(BaseModel):
    latitude: float
    """latitude of the station"""
    longitude: float
    """longitude of the station"""
    stationGlobalId: str
    """IFOPT global id of the station"""
    stationDivaId: Optional[int] = None
    """Diva id of the station, typically station identifier of IFOPT id"""
    platform: Optional[int] = None
    """Platform number, typically only with train, sbahn and ubahn services"""
    platformChanged: Optional[bool] = None
    """Whether the platform has changed"""
    place: str
    """General place of the station"""
    name: str
    """Name of the station"""
    plannedDeparture: str
    """Planned departure at the station, zoned date time"""
    departureDelayInMinutes: Optional[int] = None
    """expected delay of the departure at this station in minutes"""
    arrivalDelayInMinutes: Optional[int] = None
    """expected delay of the arrival at this station in minutes"""
    transportTypes: List[str]
    """transport types servicing this station"""
    surroundingPlanLink: str
    """unknown: presumably obsolete since deprecation of surrounding plan link"""
    occupancy: Occupancy
    """expected occupancy of the used transport medium at this station"""
    hasZoomData: bool
    """whether there is zoom data available for this station"""
    hasOutOfOrderEscalator: bool
    """aggregated info whether there is at least one broken escalator at this station"""
    hasOutOfOrderElevator: bool
    """aggregated info whether there is at least one broken elevator at this station"""


class Line(BaseModel):
    label: str
    """The line label, e.g. U4"""
    transportType: str
    """The transport type"""
    destination: str
    """Name of the destination station"""
    trainType: str
    """unknown"""
    network: str
    """provider; encountered 'ddb' for Deutsche Bahn, 'swm' for ubahn, 'mvv' for buses, 'unknown' for fussweg"""
    divaId: str
    """unknown"""
    sev: bool
    """unknown"""


class PathDescriptionItem(BaseModel):
    """unverified"""
    fromPathCoordIdx: int
    """unknown"""
    toPathCoordIdx: int
    """unknown"""
    level: int
    """unknown"""


class Info(BaseModel):
    """
    Information regarding a service in the departure board
    Examples for encountered messages:
    {'message': 'Verspätung aus vorheriger Fahrt', 'type': 'INCIDENT', 'network': 'ddb'}
    {'message': 'Reparatur an einem Signal', 'type': 'INCIDENT', 'network': 'ddb'}
    """
    message: str
    """The message text"""
    type: str
    """Type of the message: encountered 'INCIDENT'"""
    network: str
    """unknown: provider of the message, encountered 'ddb'"""


class Part(BaseModel):
    from_: Station = Field(..., alias="from")
    """Station information about the starting station in this part"""
    to: Station
    """Station information about the destination station in this part"""
    intermediateStops: List[Station]
    """Station information about the intermediate stops (excl. start and end)"""
    noChangeRequired: bool
    """unknown: always false?"""
    line: Line
    """Information about the line servicing this part of the connection"""
    pathPolyline: str
    """Polyline of the traveled part to display on a map"""
    interchangePathPolyline: str
    """Polyline of the interchange to the next part to display on a map"""
    interchangePathDistance: Optional[float] = None
    """Traveled distance in meters of this parts interchange path only (not linear distance)"""
    interchangePathDurationInMinutes: Optional[int] = None
    """Time needed for the interchange in minutes"""
    changeStatus: Optional[str] = None
    """unknown: encountered 'OK'"""
    pathDescription: List[PathDescriptionItem]
    """unknown: always empty?"""
    exitLetter: str
    """Identification letter of the exit to exit the building from the previous part to start this part"""
    distance: float
    """Traveled distance of this part in meters (not linear distance)"""
    occupancy: Occupancy
    """Expected occupancy of the transport medium"""
    messages: List
    """unknown: empty; messages displayed at mvg.de are preloaded and then mapped to the line"""
    infos: List[Info]
    """unknown: empty"""
    realTime: bool
    """unknown: presumably whether the departure times are based on real time information"""


class TicketingInformation(BaseModel):
    zones: List[int]
    """Zones traversed in this connection. Zone M is 0."""
    alternativeZones: List
    """unknown"""
    unifiedTicketIds: List[str]
    """unknown"""


class Connection(BaseModel):
    """
    A single connection between the origin and destination.
    """
    uniqueId: int
    """A unique id to identify the connection. Does not change across requests."""
    parts: List[Part]
    """List of movements in the connection with changeovers in between."""
    ticketingInformation: TicketingInformation
    """Information about pricing and suggested tickets"""
    distance: float
    """The travelled distance in meters (not linear distance)"""
    bannerHash: str
    """unknown: empty"""
    refreshId: str
    """unknown"""


class Connections(RootModel):
    """A list of connections as returned by the API."""
    root: List[Connection]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
