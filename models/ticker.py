import re
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, validator


class Station(BaseModel):
    id: str
    name: str

    @classmethod
    @validator("id")
    def valid_id(cls, _id):
        if re.fullmatch(r"^[a-z]{2}:\d{5}:\d{1,5}", _id) is None:
            raise ValueError(f"{_id} is not a valid id")
        return _id


class Slim(BaseModel):
    id: str
    title: str


class SlimList(BaseModel):
    __root__: Optional[List[Slim]]


class Line(BaseModel):
    id: str
    name: str
    typeOfTransport: str
    stations: Optional[List[Station]]
    direction: str


class IncidentDurationItem(BaseModel):
    fromDate: Optional[datetime]
    toDate: Optional[datetime]


class ActiveDuration(BaseModel):
    fromDate: Optional[datetime]
    toDate: Optional[datetime]


class Link(BaseModel):
    name: str
    href: str


class DownloadLink(BaseModel):
    id: str
    minType: Optional[str]
    name: str


class Ticker(BaseModel):
    id: str
    type: str
    title: str
    text: Optional[str] = None
    htmlText: Optional[str] = None
    lines: Optional[List[Line]] = None
    incidents: Optional[List[str]] = None
    links: Optional[List[Link]] = None
    downloadLinks: Optional[List[DownloadLink]] = None
    incidentDuration: Optional[List[IncidentDurationItem]] = None
    activeDuration: Optional[ActiveDuration] = None
    modificationDate: Optional[datetime]


class TickerList(BaseModel):
    __root__: List[Ticker]
