from __future__ import annotations

import builtins
from enum import Enum
from typing import List, Optional
import logging

from pydantic import field_validator, BaseModel, RootModel

from mvg_api.v3.network import NetworkLine
from mvg_api.v3.schemas import create_flexible_enum_validator, MessageType, StationTransportType

logger = logging.getLogger("mvg_api.v3.schemas.ticker")
logger.setLevel(logging.DEBUG)


class TickerMessageType(Enum):
    """Type of the ticker message."""
    DISRUPTION = "DISRUPTION"
    PLANNED = "PLANNED"


class Station(BaseModel):
    """Station on a line affected by the message"""
    id: str
    """IFOPT global id of the station"""
    name: str
    """Name of the station"""


class Line(BaseModel):
    """Line affected by the message"""
    id: str
    """The line label, without char e.g. 4 (for U4)"""
    name: str
    """The line label, e.g. U4"""
    typeOfTransport: str
    """The transport type; however, different identifiers are used: UBAHN is METRO"""
    stations: List[Station]
    """Stations of the line; presumably limiting to stations affected by this message"""
    direction: str
    """Direction of the line; encountered '1' and '2'; presumably mapped to GTFS H(infahrt) and R(ückfahrt)"""

    def to_network_line(self):
        """Converts this line descriptor to the standardized network line"""
        return NetworkLine.of_any(self)


class IncidentType(Enum):
    METRO = "METRO"
    TRAM = "TRAM"
    BUS = "BUS"
    MAIN_LINE = "MAIN_LINE"  # Stammstrecke
    UNKNOWN = "UNKNOWN"

    def to_station_transport_type(self) -> StationTransportType:
        """Returns the station transport type corresponding to the incidents type"""
        mapping = {
            IncidentType.METRO: StationTransportType.UBAHN,
            IncidentType.TRAM: StationTransportType.TRAM,
            IncidentType.BUS: StationTransportType.BUS,
            IncidentType.MAIN_LINE: StationTransportType.SBAHN,
            IncidentType.UNKNOWN: StationTransportType.SBAHN,
        }
        return mapping[self]


class DownloadLink(BaseModel):
    id: str
    """A uuid with some suffix, presumably to internally identify the resource. Access the resource under https://www.mvg.de/api/ems/tickers/file/$id"""
    name: str
    """Name of the link to display"""
    mimeType: str
    """Mime type of the referenced file"""


class IncidentDurationItem(BaseModel):
    """Duration specification of when the message applies"""
    fromDate: str
    """Begin datetime"""
    toDate: Optional[str]
    """End datetime"""


class ActiveDuration(BaseModel):
    """Duration specification of when the message is public (i.e. always if retrieved from the API)"""
    fromDate: str
    """Begin datetime"""
    toDate: Optional[str]
    """End datetime"""


class Message(BaseModel):
    """A message about service disruptions, both planned disruptions and unplanned incidents."""
    id: str
    """A UUID, presumably to identify the message during its lifetime"""
    type: TickerMessageType
    """Type of the message: DISRUPTION (unplanned or important) or PLANNED (planned)"""
    title: str
    """A short-ish title describing the message"""
    text: str
    """A (sometimes very) long description, formatted has html (even though there is also htmlText). It may contain links to pages with more information."""
    htmlText: str
    """A (sometimes very) long description, formatted has html. It may contain links to pages with more information."""
    lines: List[Line]
    """Lines affected by the message"""
    incidents: List[IncidentType]
    """General incident types, presumably as wrapper for multiple lines of the same transport type"""
    links: List
    """unknown: empty"""
    downloadLinks: List[DownloadLink]
    """Links to e.g. maps describing changes in the line path"""
    incidentDuration: List[IncidentDurationItem]
    """Durations where the described incident is in effect (e.g. multiple ranges of construction works)."""
    activeDuration: ActiveDuration
    """Duration during which the message should be displayed."""
    modificationDate: str
    """Modification date, presumably of the last edit, as datetime"""

    def incidents_to_stt(self) -> List[StationTransportType]:
        """Returns the incident types as list of station transport types"""
        return [i.to_station_transport_type() for i in self.incidents if isinstance(i, IncidentType)]

    _validate_type = field_validator('type', mode='before')(create_flexible_enum_validator(TickerMessageType))
    _validate_incidents = field_validator('incidents', mode='before')(
        create_flexible_enum_validator(IncidentType, is_list=True))

    def type_common(self) -> MessageType:
        """Obtain common representation of a message type."""
        if self.type == TickerMessageType.DISRUPTION:
            return MessageType.INCIDENT
        if self.type == TickerMessageType.PLANNED:
            return MessageType.SCHEDULE_CHANGE
        logger.warning("Unknown ticker message type %s", self.type)
        return None


class Messages(RootModel):
    """A list of ticker messages as returned by the API"""
    root: List[Message]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)

    def sorted(self, *, key=None, reverse: bool = False) -> Messages:
        """
        Sorts the messages to present them in a more sensible ordering by transport type and linenumber.
        :param key: key to sort with, default to sorting by type and then network line.
        """
        if key is None:
            key = Messages._default_sort_key
        return Messages(builtins.sorted(self.root, key=key, reverse=reverse))

    @staticmethod
    def _default_sort_key(m: Message):
        type_order = {
            MessageType.INCIDENT:        0,
            MessageType.SCHEDULE_CHANGE: 1,
        }
        type_rank = type_order.get(m.type, 5)
        lines = builtins.sorted([l.to_network_line() for l in m.lines])

        return (type_rank, lines[0])
