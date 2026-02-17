from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union
import logging

from pydantic import field_validator, BaseModel, RootModel

from mvg_api.v3.schemas import create_flexible_enum_validator, MessageType

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
    type: Union[TickerMessageType, str]
    """Type of the message: DISRUPTION (unplanned or important) or PLANNED (planned)"""
    title: str
    """A short-ish title describing the message"""
    text: str
    """A (sometimes very) long description, formatted has html (even though there is also htmlText). It may contain links to pages with more information."""
    htmlText: str
    """A (sometimes very) long description, formatted has html. It may contain links to pages with more information."""
    lines: List[Line]
    """Lines affected by the message"""
    incidents: List[str]
    """unknown: empty"""
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

    _validate_type = field_validator('type', mode='before')(create_flexible_enum_validator(TickerMessageType))

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

    def sorted(self, *, key=lambda v: "" if not v.lines else v.lines[0].label.rjust(5, "0"), reverse: bool = False) -> Messages:
        """
        Sorts the messages to present them in a more sensible ordering.
        :param key: key to sort with, default to sorting by label.
        """
        return Messages(sorted(self.root, key=key, reverse=reverse))
