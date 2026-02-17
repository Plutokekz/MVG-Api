from enum import Enum
from typing import Union, Type, List

import logging

logger = logging.getLogger("mvg_api.v3.schemas")
logger.setLevel(logging.DEBUG)


def create_flexible_enum_validator(enum_class: Type[Enum], is_list: bool = False):
    """
    Factory function to create a validator for flexible enum handling.
    With this validator and the property type Union[the_enum, str] it is possible to parse an API result to a
    well-known enum instance, but not fail when a value is encountered that is not present in the enum.
    In that case, the value is assigned as plain string to the property.
    """
    def validate_single(v):
        if isinstance(v, enum_class):
            return v
        if isinstance(v, str):
            try:
                return enum_class(v)
            except ValueError:
                logger.warning("Unknown %s value '%s'. Known values: %s. Using raw string.",
                               enum_class.__name__, v, ",".join([e.value for e in enum_class]))
                return v
        return v

    def validator(v):
        if is_list:
            if not isinstance(v, list):
                raise ValueError(f"Expected list, got {type(v)}")
            return [validate_single(item) for item in v]
        else:
            return validate_single(v)

    return validator


class Occupancy(str, Enum):
    """Occupancy of a service in general or at a specific station."""
    UNKNOWN = "UNKNOWN"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class OfferedTransportType(Enum):
    """
    Transport types offered at a station.
    This is a limited set of transport types compared to the transport types that can be found on a service line.
    """
    TRAM = "TRAM"
    BUS = "BUS"
    UBAHN = "UBAHN"
    SBAHN = "SBAHN"
    BAHN = "BAHN"
    SCHIFF = "SCHIFF"


class TariffZones:
    """Common representation of tariff zones"""

    def __init__(self, zones: Union[str, List[int]]):
        """Converts tariff zone given as string or list of integers to a common representation"""
        if zones == None or zones == "":
            self._zones = []
        elif type(zones) == str:
            self._zones = [int(z) for z in zones.replace("m", "0").replace("M", "0").split('|')]
        elif type(zones) == list and all([type(z) == int for z in zones]):
            self._zones = zones
        else:
            self._zones = []
            logger.error("Invalid argument to TariffZones: type=%s zones=%s", type(zones), zones)
        self._zones.sort()
        for z in self._zones:
            if z not in range(0, 13):
                logger.warning("Encountered unknown tariff zone %s", z)
        self._zones = ["M" if z == 0 else str(z) for z in self._zones]
        logger.debug("Zones [%s]", ",".join(self._zones))

    def __iter__(self):
        return iter(self._zones)

    def __len__(self):
        return len(self._zones)

    def __getitem__(self, index):
        return self._zones[index]
