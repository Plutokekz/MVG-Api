from __future__ import annotations

import builtins
from enum import Enum
from typing import List, Optional

from pydantic import field_validator, BaseModel, Field, RootModel

from mvg_api.v3.network import NetworkLine
from mvg_api.v3.schemas import create_flexible_enum_validator, MessageType, StationTransportType


class Link(BaseModel):
    """Link to an external resource, typically a pdf showing a line change or a construction timetable"""
    text: str
    """Display text of the link name"""
    url: str
    """URL to the resource"""


class Line(BaseModel):
    "Line affected by the message"
    label: str
    """The line label, e.g. U4"""
    transportType: str
    """The transport type"""
    network: str
    """provider; encountered 'ddb' for Deutsche Bahn, 'swm' for ubahn, 'mvv' for buses, 'unknown' for fussweg"""
    divaId: Optional[str] = None
    """unknown"""
    sev: bool
    """unknown"""

    def to_network_line(self):
        """Converts this line descriptor to the standardized network line"""
        return NetworkLine.of_any(self)


class PublicationDuration(BaseModel):
    """Duration specification of when the message is public (i.e. always if retrieved from the API)"""
    from_: int = Field(..., alias="from")
    """Begin timestamp in milliseconds"""
    to: Optional[int] = None
    """End timestamp in milliseconds"""


class IncidentDuration(BaseModel):
    """Duration specification of when the message applies"""
    from_: int = Field(..., alias="from")
    """Begin timestamp in milliseconds"""
    to: Optional[int] = None
    """End timestamp in milliseconds"""


class EventType(Enum):
    UBAHN = "UBAHN"
    BUS = "BUS"
    TRAM = "TRAM"
    SBAHN = "SBAHN"
    STAMMSTRECKE = "STAMMSTRECKE"

    def to_station_transport_type(self) -> StationTransportType:
        """Returns the station transport type corresponding to the incidents type"""
        mapping = {
            EventType.UBAHN: StationTransportType.UBAHN,
            EventType.TRAM: StationTransportType.TRAM,
            EventType.BUS: StationTransportType.BUS,
            EventType.SBAHN: StationTransportType.SBAHN,
            EventType.STAMMSTRECKE: StationTransportType.SBAHN,
        }
        return mapping[self]


class Message(BaseModel):
    """
    A message about service disruptions, both planned disruptions and unplanned incidents.
    These are the messages shown on mvg.de for all lines.
    The website and presumably also the app cache these messages to display them in the
    departures or connections views on the respective service lines.
    """
    title: str
    """A short-ish title describing the message"""
    description: str
    """A (sometimes very) long description, formatted has html. It may contain links to pages with more information."""
    publication: int
    """Publication timestamp in milliseconds (presumably obsolete since introduction of publication duration)"""
    publicationDuration: PublicationDuration
    """Duration during which the message should be displayed. The api only returns published messages."""
    incidentDurations: List[IncidentDuration]
    """Durations where the described incident is in effect (e.g. multiple ranges of construction works)."""
    validFrom: int
    """Incident start timestamp in milliseconds (presumably obsolete since introduction of incident durations)"""
    validTo: Optional[int] = None
    """Incident end timestamp in milliseconds (presumably obsolete since introduction of incident durations)"""
    type: MessageType
    """Type of the message: INCIDENT (unplanned or important) or SCHEDULE_CHANGE (planned)"""
    provider: str
    """Provider of the information; encountered 'MVG' for mvg services (ubahn, bus<200, tram) and 'DEFAS' for sbahn, bahn, bus>=200)"""
    links: List[Link]
    """Links to e.g. maps describing changes in the line path"""
    lines: List[Line]
    """Lines affected"""
    stationGlobalIds: List[str]
    """IFOPT global ids of stations affected"""
    eventTypes: List[EventType]
    """General event types, presumably as wrapper for multiple lines of the same transport type"""

    _validate_type = field_validator('type', mode='before')(create_flexible_enum_validator(MessageType))
    _validate_transportTypes = field_validator('eventTypes', mode='before')(
        create_flexible_enum_validator(EventType, is_list=True))

    def event_types_to_stt(self) -> List[StationTransportType]:
        """Returns the messages event types as station transport types"""
        return [et.to_station_transport_type() for et in self.eventTypes]


class Messages(RootModel):
    """A list of messages as returned by the API"""
    root: List[Message]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)

    def sorted(self, *, key=None, reverse: bool = False) -> Messages:
        """
        Sorts the messages to present them in a more sensible ordering.
        :param key: key to sort with, default to sorting by label.
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
        if len(lines) > 0 and lines[0]:
            return (type_rank, lines[0])
        return (type_rank,)
