from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, RootModel


class Station(BaseModel):
    latitude: float
    longitude: float
    stationGlobalId: str
    stationDivaId: Optional[int] = None
    platform: Optional[int] = None
    platformChanged: Optional[bool] = None
    place: str
    name: str
    plannedDeparture: str
    departureDelayInMinutes: Optional[int] = None
    arrivalDelayInMinutes: Optional[int] = None
    transportTypes: List[str]
    surroundingPlanLink: str
    occupancy: str
    hasZoomData: bool
    hasOutOfOrderEscalator: bool
    hasOutOfOrderElevator: bool

    def delayInMinutes(self):
        """
        :return: in order of presence, the departure delay, the arrival delay or none.
        """
        if self.departureDelayInMinutes is not None:
            return self.departureDelayInMinutes
        if self.arrivalDelayInMinutes is not None:
            return self.arrivalDelayInMinutes
        return None


class Line(BaseModel):
    label: str
    transportType: str
    destination: str
    trainType: str
    network: str
    divaId: str
    sev: bool


class PathDescriptionItem(BaseModel):
    fromPathCoordIdx: int
    toPathCoordIdx: int
    level: int


class Part(BaseModel):
    from_: Station = Field(..., alias="from")
    to: Station
    intermediateStops: List[Station]
    noChangeRequired: bool
    line: Line
    pathPolyline: str
    interchangePathPolyline: str
    pathDescription: List[PathDescriptionItem]
    exitLetter: str
    distance: float
    occupancy: str
    messages: List
    arrivalStopPositionNumber: Optional[int] = None


class TicketingInformation(BaseModel):
    zones: List[int]
    alternativeZones: List
    unifiedTicketIds: List[str]


class Connection(BaseModel):
    uniqueId: int
    parts: List[Part]
    ticketingInformation: TicketingInformation
    distance: float
    bannerHash: str


class Connections(RootModel):
    root: List[Connection]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
