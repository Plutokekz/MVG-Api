from __future__ import annotations

from functools import total_ordering
import re
from enum import Enum
import logging

logger = logging.getLogger("apivis")
logger.setLevel(logging.DEBUG)


class NetworkTransportType(Enum):
    """
    Transport types of a network line.
    More sophisticated than station transport types, since we (need) to differentiate night services
    to style the respective line indicators and there are additional transport types like fussweg or
    sev that are not "offered" by a station.
    """

    UBAHN = "UBAHN"
    TRAM = "TRAM"
    NACHT_TRAM = "NACHT_TRAM"
    BUS = "BUS"
    EXPRESS_BUS = "EXPRESS_BUS"
    REGIONAL_BUS = "REGIONAL_BUS"
    NACHT_BUS = "NACHT_BUS"
    SBAHN = "SBAHN"
    BAHN = "BAHN"
    BAHN_FERN = "BAHN_FERN"
    SEV = "SEV"
    SCHIFF = "SCHIFF"
    PEDESTRIAN = "PEDESTRIAN"
    RUFTAXI = "RUFTAXI"
    TAXI = "TAXI"
    UNKNOWN = "UNKNOWN"


@total_ordering
class NetworkLine:
    """
    Uniform description of a specific line with transport type.
    This is necessary because the official api uses different keys to describe transport type and line label.
    """

    @classmethod
    def of_any(cls, any_line_descriptor) -> NetworkLine:
        """
        Extract transport type and line label from any line descriptor of the mvg api
        (e.g. MessageLine, TickerLine, etc), as they use different keys to name the
        corresponding variable, and returns a unified network line.
        """
        # import here to prevent circular imports
        # pylint: disable=import-outside-toplevel
        from mvg_api.v3.schemas.aushang import Aushang
        from mvg_api.v3.schemas.connection import Line as ConnectionLine
        from mvg_api.v3.schemas.departure import Departure
        from mvg_api.v3.schemas.line import Line as LineLine
        from mvg_api.v3.schemas.messages import Line as MessageLine
        from mvg_api.v3.schemas.ticker import Line as TickerLine

        if isinstance(any_line_descriptor, NetworkLine):
            return any_line_descriptor

        transport_type = ""
        line_label = ""
        train_type = ""
        details = {}
        if isinstance(any_line_descriptor, Aushang):
            transport_type = (
                any_line_descriptor.scheduleKind.value
            )  # special case because enum
            line_label = any_line_descriptor.scheduleName
        elif isinstance(any_line_descriptor, ConnectionLine):
            transport_type = any_line_descriptor.transportType
            line_label = any_line_descriptor.label
            train_type = any_line_descriptor.trainType
            details = {
                "destination": any_line_descriptor.destination,
                "trainType": any_line_descriptor.trainType,
                "network": any_line_descriptor.network,
                "divaId": any_line_descriptor.divaId,
                "sev": any_line_descriptor.sev,
            }
        elif isinstance(any_line_descriptor, Departure):
            transport_type = any_line_descriptor.transportType
            line_label = any_line_descriptor.label
            details = {
                "divaId": any_line_descriptor.divaId,
                "network": any_line_descriptor.network,
                "trainType": any_line_descriptor.trainType,
            }
        elif isinstance(any_line_descriptor, LineLine):
            transport_type = any_line_descriptor.transportType
            line_label = any_line_descriptor.label
            details = {
                "divaId": any_line_descriptor.divaId,
                "network": any_line_descriptor.network,
                "sev": any_line_descriptor.sev,
            }
        elif isinstance(any_line_descriptor, MessageLine):
            transport_type = any_line_descriptor.transportType
            line_label = any_line_descriptor.label
            details = {
                "divaId": any_line_descriptor.divaId,
                "network": any_line_descriptor.network,
                "sev": any_line_descriptor.sev,
            }
        elif isinstance(any_line_descriptor, TickerLine):
            transport_type = any_line_descriptor.typeOfTransport
            line_label = any_line_descriptor.name
            details = {
                "id": any_line_descriptor.id,
                "direction": any_line_descriptor.direction,
                "stations": ", ".join(
                    [f"{s.name} ({s.id})" for s in any_line_descriptor.stations]
                ),
            }
        else:
            logger.error(
                "Unknown line descriptor type %s with data %s",
                f"{type(any_line_descriptor).__module__}.{type(any_line_descriptor).__name__}",
                any_line_descriptor,
            )

        shared_details = {
            "transport_type": transport_type,
            "line_label": line_label,
        }
        details = shared_details | details
        return NetworkLine(transport_type, line_label, train_type, details)

    def __init__(self, transport_type, line_label, train_type="", details=None):
        """
        Takes a raw transport type from the official api and unifies it to one of NetworkTransportType.
        """

        # aushang returns NIGHT_LINE for night bus/tram but other endpoints return simply BUS or TRAM
        # manually filter them here depending on the line number into NIGHT_BUS and NIGHT_TRAM
        # night tram has orange font, night bus white

        # mvg number ranges:
        # 1-8 ubahn
        # 12-39 tram (N17-N27 nachttram)
        # X30-98 express bus
        # 50-199 bus (N40-N81 nachtbus)
        # 200- regional bus

        self.line_label = line_label
        self.train_type = train_type
        self.details = {} if details is None else details

        if "sev" in self.details and self.details["sev"]:
            self.transport_type = NetworkTransportType.SEV
            if line_label == "":  # use line label if present, otherwise fall back to tt
                self.line_label = transport_type
        elif line_label.startswith("N"):
            if int(line_label[1:]) < 40:
                self.transport_type = NetworkTransportType.NACHT_TRAM
            else:
                self.transport_type = NetworkTransportType.NACHT_BUS
        elif transport_type in ["UBAHN", "SUBWAY", "METRO"]:
            self.transport_type = NetworkTransportType.UBAHN
        elif train_type != "":  # ["ICE", "RJ"]
            self.transport_type = NetworkTransportType.BAHN_FERN
            self.line_label = f"{train_type} {line_label}"
        else:
            self.transport_type = NetworkTransportType(transport_type)

    def _sort_key(self):
        """
        :return: a sort key for this network line such that messages and similar can be sorted like it is done on mvg.de
        """
        tt = self.transport_type
        label = self.line_label

        type_order = {
            NetworkTransportType.UBAHN: 0,
            NetworkTransportType.TRAM: 1,
            NetworkTransportType.NACHT_TRAM: 2,
            NetworkTransportType.BUS: 3,
            NetworkTransportType.EXPRESS_BUS: 3,
            NetworkTransportType.REGIONAL_BUS: 3,
            NetworkTransportType.NACHT_BUS: 4,
            NetworkTransportType.SBAHN: 5,
            NetworkTransportType.BAHN: 6,
            NetworkTransportType.BAHN_FERN: 6,
        }
        type_rank = type_order.get(tt, 10)

        if type_rank == type_order[NetworkTransportType.BUS]:  # any bus
            # Numbers-first: "50" < "500" < "500X" < "9000" < "X234"
            m = re.match(r"^(\d+)(.*)", label)
            if m:
                label_key = (0, int(m.group(1)), m.group(2))
            else:
                label_key = (1, 0, label)
        else:
            label_key = (0, 0, label)

        return (type_rank, *label_key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NetworkLine):
            return NotImplemented
        return self._sort_key() == other._sort_key()

    def __lt__(self, other: "NetworkLine") -> bool:
        if not isinstance(other, NetworkLine):
            return NotImplemented
        return self._sort_key() < other._sort_key()

    def title_str(self) -> str:
        """
        :return: The details of this line html formatted multiline string.
        """
        title = ""
        if self.details != {}:
            for k, v in self.details.items():
                title += f"{k}: {v}&#010;"
        return title

    def line_color(
        self, tram_colors: bool = False
    ) -> (
        str
    ):  # pylint: disable=too-many-return-statements,too-many-branches,too-many-statements
        """
        :param tram_colors: true when individual tram line colors should be returned or false for the generic tram red.
        :return: the color primarily associated with this network line.
        """
        if self.transport_type == NetworkTransportType.UBAHN:
            if self.line_label == "U1":
                return "#52822f"
            if self.line_label == "U2":
                return "#c2243b"
            if self.line_label == "U3":
                return "#ec6725"
            if self.line_label == "U4":
                return "#00a984"
            if self.line_label == "U5":
                return "#bb7a00"
            if self.line_label == "U6":
                return "#0065ad"
            if self.line_label == "U7":
                return "#52822f"  # split with U2 #c2243b
            if self.line_label == "U8":
                return "#c2243b"  # split with U3 #ec6725
        if self.transport_type == NetworkTransportType.TRAM:
            if tram_colors:
                if self.line_label == "12":
                    return "#95348b"
                if self.line_label == "14":
                    return "#e5007c"
                if self.line_label == "16":
                    return "#0064ad"
                if self.line_label == "17":
                    return "#8a553e"
                if self.line_label == "18":
                    return "#08a536"
                if self.line_label == "19":
                    return "#e2000e"
                if self.line_label == "20":
                    return "#10bae6"
                if self.line_label == "21":
                    return "#bb7900"
                if self.line_label == "23":
                    return "#bbce00"
                if self.line_label == "25":
                    return "#f1909c"
                if self.line_label == "27":
                    return "#f7a500"
                if self.line_label == "28":
                    return "#f7a500"
            return "#e30613"  # tram rot
        if self.transport_type == NetworkTransportType.NACHT_TRAM:
            return "#000000"
        if self.transport_type == NetworkTransportType.BUS:
            if self.line_label == "X80":
                return "#1a6eb2"
            if self.line_label == "X30":
                return "#718873"
            return "#00586a"
        if self.transport_type == NetworkTransportType.EXPRESS_BUS:
            return "#4e7e6c"
        if self.transport_type == NetworkTransportType.REGIONAL_BUS:
            if self.line_label == "X200":
                return "#cd8236"
            if self.line_label == "X201":
                return "#009658"
            if self.line_label == "X202":
                return "#c4047b"
            if self.line_label == "X203":
                return "#0094ce"
            if self.line_label == "X204":
                return "#a47dae"
            if self.line_label == "X205":
                return "#00776f"
            if self.line_label == "X206":
                return "#007c73"
            if self.line_label == "X208":
                return "#75ae58"
            if self.line_label == "X320":
                return "#3b9c3a"
            if self.line_label == "X660":
                return "#db6d3a"
            if self.line_label == "X730":
                return "#489d2e"
            if self.line_label == "X731":
                return "#b60065"
            if self.line_label == "X732":
                return "#0071aa"
            if self.line_label == "X733":
                return "#beb000"
            if self.line_label == "X910":
                return "#ac8055"
            return "#00586a"  # was #003255 some time ago
        if self.transport_type == NetworkTransportType.NACHT_BUS:
            return "#000000"
        if self.transport_type == NetworkTransportType.SBAHN:
            if self.line_label == "S1":
                return "#1b9fc6"
            if self.line_label == "S2":
                return "#69a338"
            if self.line_label == "S3":
                return "#973083"
            if self.line_label == "S4":
                return "#e23331"
            if self.line_label == "S5":
                return "#005e82"
            if self.line_label == "S6":
                return "#008d5e"
            if self.line_label == "S7":
                return "#883b32"
            if self.line_label == "S8":
                return "#2d2b29"
            if self.line_label == "S20":
                return "#ee5973"
            return "#008d4f"  # random sbahn lines like S999, S8/9, S6/8
        if self.transport_type == NetworkTransportType.BAHN:
            return "#000000"
        if self.transport_type == NetworkTransportType.BAHN_FERN:
            return "#000000"
        if self.transport_type == NetworkTransportType.SEV:
            return "#97378c"
        if self.transport_type == NetworkTransportType.PEDESTRIAN:
            return "#4471b5"
        if self.transport_type == NetworkTransportType.RUFTAXI:
            return "#4682b4"
        if self.transport_type == NetworkTransportType.TAXI:
            return "#fff104"
        if self.transport_type == NetworkTransportType.UNKNOWN:
            return "#fd0097"
        logger.warning(
            "No-yet-known transport type '%s' and line '%s' encountered",
            self.transport_type,
            self.line_label,
        )
        return "#fd0097"

    def line_color_split(self) -> str:
        """
        :return: the secondary fill color of the line indicator for this network line.
        Encountered on U7 and U8 because there is a split between e.g. U1 and U2 that makes up U7.
        """
        if self.transport_type == NetworkTransportType.UBAHN:
            if self.line_label == "U7":
                return "#c2243b"
            if self.line_label == "U8":
                return "#f1743c"
        return ""

    def text_color(self) -> str:
        """
        :return: the text color of the line badge for this network line.
        """
        if self.transport_type == NetworkTransportType.NACHT_TRAM:
            return "#ffb638"
        if self.transport_type == NetworkTransportType.SBAHN:
            if self.line_label == "S8":
                return "#fdce32"
        if self.transport_type == NetworkTransportType.BAHN_FERN:
            return "#ec0016"
        if self.transport_type == NetworkTransportType.SEV:
            return "#97378c"
        if self.transport_type == NetworkTransportType.TAXI:
            return "#000000"
        return "#ffffff"

    def color_inverted(self, tram_colors: bool = False) -> bool:
        """
        :return: True if foreground and background are inverted except for a border around the background in the background color.
        """
        if self.transport_type == NetworkTransportType.TRAM:
            if tram_colors:  # do not invert tram if no tram_colors specified
                if self.line_label == "28":
                    return True
                if self.line_label == "29":
                    return True
        return False


def line_color(any_line_descriptor):
    """
    :param any_line_descriptor: a line descriptor of e.g. a connection or a network line
    :return: the fill color of a network line
    """
    nl = NetworkLine.of_any(any_line_descriptor)
    return nl.line_color()


def zone_color(zone: str) -> str:  # pylint: disable=too-many-return-statements
    """
    Returns the color of a network zone.
    Input is accepted as int, sting and upper/lowercase (m only).
    """
    if zone in [0, "0", "m", "M"]:
        return "#006b8f"
    if zone in [1, "1"]:
        return "#c2b500"
    if zone in [2, "2"]:
        return "#b82040"
    if zone in [3, "3"]:
        return "#63c0d5"
    if zone in [4, "4"]:
        return "#00793b"
    if zone in [5, "5"]:
        return "#f39415"
    if zone in [6, "6"]:
        return "#0061ab"
    if zone in [7, "7"]:
        return "#d04d21"
    if zone in [8, "8"]:
        return "#589b97"
    if zone in [9, "9"]:
        return "#9f8c11"
    if zone in [10, "10"]:
        return "#5da780"
    if zone in [11, "11"]:
        return "#ab3169"
    if zone in [12, "12"]:
        return "#0077a7"

    logger.warning("Unknown zone '%s' encountered", zone)
    return "#fd0097"
