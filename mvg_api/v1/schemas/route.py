import re
from enum import Enum
from typing import List, Optional, Iterator

from pydantic import BaseModel, Field, field_validator, RootModel


class LocationType(Enum):
    STATION = "STATION"
    ADDRESS = "ADDRESS"
    POI = "POI"


class Location(BaseModel):
    type: LocationType
    latitude: float
    longitude: float

    place: str
    globalId: Optional[str] = None
    divaId: Optional[int] = None
    name: Optional[str] = None
    hasZoomData: Optional[bool] = None
    tariffZones: Optional[str] = None
    aliases: Optional[str] = None
    transportTypes: Optional[List[str]] = None
    surroundingPlanLink: Optional[str] = None

    @classmethod
    @field_validator("globalId")
    def valid_id(cls, _id):
        if re.fullmatch(r"^[a-z]{2}:\d{5}:\d{1,5}", _id) is None:
            raise ValueError(f"{_id} is not a valid id")
        return _id


class SapTicketMappingDto(BaseModel):
    sapId: int
    sapName: Optional[str]
    sapPrice: Optional[str]
    displayTitleDe: Optional[str]
    displayTitleEn: Optional[str]
    displaySubtitleDe: Optional[str]
    displaySubtitleEn: Optional[str]
    efaId: Optional[str]
    type: Optional[str]
    availableATM: Optional[bool]
    availableMobileATM: Optional[bool]
    availableAPP: Optional[bool]
    ticketAggregationGroup: Optional[str]
    tarifLevel: Optional[str]
    zones: Optional[str]


class LocationList(RootModel):
    root: List[Location]

    def __iter__(self) -> Iterator[Location]:
        return iter(self.root)

    def __getitem__(self, item) -> Location:
        return self.root[item]

    def __len__(self):
        return len(self.root)


class ConnectionLocation(BaseModel):
    latitude: float
    longitude: float
    stationGlobalId: str
    stationDivaId: int
    place: str
    name: str
    plannedDeparture: str
    departureDelayInMinutes: Optional[int] = None
    transportTypes: List[str]
    surroundingPlanLink: str
    occupancy: str
    hasZoomData: bool
    hasOutOfOrderEscalator: bool
    hasOutOfOrderElevator: bool
    platform: Optional[int] = None


class Line(BaseModel):
    label: str
    transportType: str
    destination: str
    trainType: str
    network: str
    sev: bool


class PathDescriptionItem(BaseModel):
    fromPathCoordIdx: int
    toPathCoordIdx: int
    level: int


class Part(BaseModel):
    from_: ConnectionLocation = Field(..., alias="from")
    to: ConnectionLocation
    intermediateStops: List[ConnectionLocation]
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


class Connections(BaseModel):
    connectionList: List[Connection]
