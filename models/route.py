import datetime
import re
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Lines(BaseModel):
    tram: Optional[List[str]]
    nachttram: Optional[List[str]]
    sbahn: Optional[List[str]]
    ubahn: Optional[List[str]]
    bus: Optional[List[str]]
    nachtbus: Optional[List[str]]
    otherlines: Optional[List[str]]


class LocationType(Enum):
    STATION = "station"
    ADDRESS = "address"


class Products(Enum):
    BUS = "BUS"
    TRAM = "TRAM"
    UBAHN = "UBAHN"
    SBAHN = "SBAHN"
    BAHN = "BAHN"


class Location(BaseModel):
    id: Optional[str]
    type: LocationType
    latitude: float
    longitude: float
    divaId: Optional[int]
    place: str
    name: Optional[str]
    hasLiveData: Optional[bool]
    hasZoomData: Optional[bool]
    products: Optional[List[Products]]
    efaLon: Optional[float]
    efaLat: Optional[float]
    link: Optional[str]
    tariffZones: Optional[str]
    occupancy: Optional[str]
    lines: Optional[Lines]
    aliases: Optional[str]
    poi: Optional[bool]
    street: Optional[str]

    @classmethod
    @validator("id")
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


class Connection(BaseModel):
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


class Connections(BaseModel):
    connectionList: Optional[List[Connection]]


class LocationList(BaseModel):
    locations: Optional[List[Location]]
