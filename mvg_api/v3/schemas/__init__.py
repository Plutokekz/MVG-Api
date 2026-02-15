from enum import Enum
from typing import Union, Optional, Type

import logging

logger = logging.getLogger("mvg_api.v3.schemas")


def create_flexible_enum_validator(enum_class: Type[Enum]):
    """Factory function to create a validator for flexible enum handling"""
    def validator(v):
        if isinstance(v, enum_class):
            return v
        if isinstance(v, str):
            try:
                return enum_class(v)
            except ValueError:
                logger.warning(
                    f"Unknown {enum_class.__name__} value '{v}'. "
                    f"Known values: {[e.value for e in enum_class]}. "
                    f"Using raw string.",
                    UserWarning
                )
                return v
        return v
    return validator
