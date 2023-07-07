from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class BaseStation(BaseModel):
    id: str
    name: str


class Station(BaseStation):
    pass


class Line(BaseStation):
    typeOfTransport: str
    stations: List[Station]
    direction: str


class Link(BaseModel):
    name: str
    href: str


class DownloadLink(BaseModel):
    id: str
    name: str
    mimeType: str


class IncidentDurationItem(BaseModel):
    fromDate: str
    toDate: Optional[str]


class ActiveDuration(BaseModel):
    fromDate: str
    toDate: Optional[str]


class Message(BaseModel):
    id: str
    type: str
    title: str
    text: str
    htmlText: str
    lines: List[Line]
    incidents: List[str]
    links: List[Link]
    downloadLinks: List[DownloadLink]
    incidentDuration: List[IncidentDurationItem]
    activeDuration: ActiveDuration
    modificationDate: str


class Messages(BaseModel):
    __root__: List[Message]
