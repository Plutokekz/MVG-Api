from __future__ import annotations

import builtins
from enum import Enum
from typing import List
from pydantic import BaseModel, RootModel, field_validator

from mvg_api.v3.network import NetworkLine
from mvg_api.v3.schemas import create_flexible_enum_validator


class AushangScheduleKind(Enum):
    STATION_OVERVIEW_MAP = "STATION_OVERVIEW_MAP"
    """general overview map of a station, and nearby streets and institutions"""
    CONTEXT_MAP = "CONTEXT_MAP"
    """shows the different stop points of e.g. busses or tram lines"""
    SUBWAY = "SUBWAY"
    TRAM = "TRAM"
    BUS = "BUS"
    NIGHT_LINE = "NIGHT_LINE"

    def is_station_overview_map(self):
        """Returns true if the aushang is the larger station overview map."""
        return self == AushangScheduleKind.STATION_OVERVIEW_MAP

    def is_context_map(self):
        """Returns true if the aushang is the stop point context map."""
        return self == AushangScheduleKind.CONTEXT_MAP


class Aushang(BaseModel):
    """A single aushang pdf document like a map or timetable"""
    uri: str
    """The URI to the pdf document, typically hosted at mvg.de"""
    scheduleKind: AushangScheduleKind
    """Type of aushang; a transport type or aushang specific constants"""
    scheduleName: str
    """The line number in context with the transport type in the schedule kind"""
    direction: str
    """Nicetext description of the aushang; might include validity information for timetables during e.g. construction work"""

    # flexible validators such that pydantic does not fail if a value that is not in the enum is encountered
    _validate_scheduleKind = field_validator('scheduleKind', mode='before')(create_flexible_enum_validator(AushangScheduleKind))

    def to_network_line(self):
        """
        Converts this line descriptor to the standardized network line.
        :return: a network like or none if this aushang is a context map or a station overview map
        """
        if self.scheduleKind in [AushangScheduleKind.CONTEXT_MAP, AushangScheduleKind.STATION_OVERVIEW_MAP]:
            return None
        return NetworkLine.of_any(self)


class Aushaenge(RootModel):
    """A list of aushaenge as returned by the API"""
    root: List[Aushang]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)

    def sorted(self, *, key=None, reverse: bool = False) -> Aushaenge:
        """
        Sorts the aushang.
        :param key: key to sort with, default to sorting by aushang type (maps first) then line.
        """
        if key is None:
            key = Aushaenge._default_sort_key
        return Aushaenge(builtins.sorted(self.root, key=key, reverse=reverse))

    @staticmethod
    def _default_sort_key(a: Aushang):
        type_order = {
            AushangScheduleKind.STATION_OVERVIEW_MAP: 0,
            AushangScheduleKind.CONTEXT_MAP:          1,
        }
        type_rank = type_order.get(a.scheduleKind, 2)
        return (type_rank, a.to_network_line())
