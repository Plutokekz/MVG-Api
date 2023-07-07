from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Link(BaseModel):
    text: str
    url: str


class Line(BaseModel):
    label: str
    transportType: str
    network: str
    sev: bool


class Message(BaseModel):
    title: str
    description: str
    publication: int
    validFrom: int
    validTo: int
    type: str
    provider: str
    links: List[Link]
    lines: List[Line]
    stationGlobalIds: List[str]
    eventTypes: List[str]


class Messages(BaseModel):
    __root__: List[Message]
