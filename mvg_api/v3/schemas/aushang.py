from __future__ import annotations

from typing import List

from pydantic import BaseModel, RootModel


class Aushang(BaseModel):
    """A single aushang pdf document like a map or timetable"""
    uri: str
    """The URI to the pdf document, typically hosted at mvg.de"""
    scheduleKind: str
    """
    Type of aushang; a transport type or the constants
    * STATION_OVERVIEW_MAP for the general overview map of a station, and nearby streets and institutions
    * CONTEXT_MAP that shows the different stop points of e.g. busses or tram lines
    """
    scheduleName: str
    """The line number in context with the transport type"""
    direction: str
    """Textual description of the aushang; might include validity information for timetables during e.g. construction work"""


class Aushaenge(RootModel):
    """A list of aushaenge as returned by the API"""
    root: List[Aushang]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
