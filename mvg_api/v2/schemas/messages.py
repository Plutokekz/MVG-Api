from __future__ import annotations

from typing import List

from pydantic import BaseModel, RootModel


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


class Messages(RootModel):
    root: List[Message]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
