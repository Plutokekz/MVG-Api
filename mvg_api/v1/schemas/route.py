import datetime
import re
from enum import Enum
from typing import List, Optional, Iterator

from pydantic import BaseModel, Field, field_validator, RootModel


class Lines(BaseModel):
    tram: Optional[List[str]]
    nachttram: Optional[List[str]]
    sbahn: Optional[List[str]]
    ubahn: Optional[List[str]]
    bus: Optional[List[str]]
    nachtbus: Optional[List[str]]
    otherlines: Optional[List[str]]


class LocationType(Enum):
    STATION = "STATION"
    ADDRESS = "ADDRESS"
    POI = "POI"


class Products(Enum):
    BUS = "BUS"
    TRAM = "TRAM"
    UBAHN = "UBAHN"
    SBAHN = "SBAHN"
    BAHN = "BAHN"


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


class PathItem(BaseModel):
    type: str
    latitude: float
    longitude: float


class PathDescription(BaseModel):
    from_: int = Field(None, alias="from")
    to: int
    level: int


class InterchangePath(BaseModel):
    latitude: float
    longitude: float
    type: str


class Stop(BaseModel):
    arrDelay: Optional[int]
    cancelled: bool
    delay: Optional[int]
    time: int
    location: Location


class ConnectionPart(BaseModel):
    stops: Optional[List[Stop]]
    from_: Location = Field(None, alias="from")
    to: Location
    path: Optional[List[PathItem]]
    pathDescription: Optional[List[PathDescription]]
    interchangePath: Optional[List[InterchangePath]] = None
    departure: float
    arrival: float
    delay: Optional[float]
    arrDelay: Optional[float]
    cancelled: bool
    product: Optional[Products]
    label: Optional[str]
    network: Optional[str]
    connectionPartType: Optional[str]
    serverId: Optional[str]
    destination: Optional[str]
    lineDirection: Optional[str]
    sev: Optional[bool]
    zoomNoticeDeparture: Optional[bool]
    zoomNoticeArrival: Optional[bool]
    zoomNoticeDepartureEscalator: Optional[bool]
    zoomNoticeArrivalEscalator: Optional[bool]
    zoomNoticeDepartureElevator: Optional[bool]
    zoomNoticeArrivalElevator: Optional[bool]
    departurePlatform: Optional[str]
    departureStopPositionNumber: Optional[int]
    arrivalPlatform: Optional[str]
    arrivalStopPositionNumber: Optional[int]
    noChangingRequired: Optional[bool]
    fromId: Optional[str]
    departureId: Optional[str]
    occupancy: Optional[str]


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


class _Connection(BaseModel):
    zoomNoticeFrom: Optional[bool]
    zoomNoticeTo: Optional[bool]
    zoomNoticeFromEscalator: Optional[bool]
    zoomNoticeToEscalator: Optional[bool]
    zoomNoticeFromElevator: Optional[bool]
    zoomNoticeToElevator: Optional[bool]
    from_: Location = Field(None, alias="from")
    to: Location
    departure: Optional[datetime.datetime]
    arrival: Optional[datetime.datetime]
    connectionPartList: List[ConnectionPart]
    efaTicketIds: Optional[List[str]]
    serverId: Optional[int]
    ringFrom: Optional[int]
    ringTo: Optional[int]
    sapTicketMappingDtos: Optional[List[SapTicketMappingDto]]
    oldTarif: Optional[bool]


class _Connections(BaseModel):
    connectionList: Optional[List[_Connection]]


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
