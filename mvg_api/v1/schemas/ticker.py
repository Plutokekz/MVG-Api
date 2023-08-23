import re
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, RootModel, field_validator


class Station(BaseModel):
    id: str
    name: str

    @classmethod
    @field_validator("id")
    def valid_id(cls, _id):
        if re.fullmatch(r"^[a-z]{2}:\d{5}:\d{1,5}", _id) is None:
            raise ValueError(f"{_id} is not a valid id")
        return _id


class Slim(BaseModel):
    id: str
    title: str


class SlimList(RootModel):
    root: Optional[List[Slim]]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)


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
    name: str
    minType: Optional[str] = None


class Ticker(BaseModel):
    id: str
    type: str
    title: str
    text: Optional[str] = None
    htmlText: Optional[str] = None
    lines: Optional[List[Line]] = None
    incidents: Optional[List[str]] = None
    links: Optional[List[Link]] = None
    downloadLinks: Optional[List[Optional[DownloadLink]]] = None
    incidentDuration: Optional[List[IncidentDurationItem]] = None
    activeDuration: Optional[ActiveDuration] = None
    modificationDate: Optional[datetime] = None


class TickerList(RootModel):
    root: List[Ticker]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
