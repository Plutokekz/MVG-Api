from enum import Enum
from typing import Union, Optional, Type

import logging

logger = logging.getLogger("mvg_api.v3.schemas")
logger.setLevel(logging.DEBUG)


def create_flexible_enum_validator(enum_class: Type[Enum]):
    """
    Factory function to create a validator for flexible enum handling.
    With this validator and the property type Union[the_enum, str] it is possible to parse an API result to a
    well-known enum instance, but not fail when a value is encountered that is not present in the enum.
    In that case, the value is assigned as plain string to the property.
    """
    def validator(v):
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
    return validator
