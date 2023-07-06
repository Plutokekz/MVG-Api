from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class TransportDevice(BaseModel):
    description: str
    identifier: str
    lastUpdate: Optional[int]
    name: str
    status: str
    type: str
    xcoordinate: int
    ycoordinate: int
    planned: Any


class StationTransportDevices(BaseModel):
    efaId: int
    name: str
    transportDevices: List[TransportDevice]
    aggregatedStatusROLLTREPPE: str
    aggregatedStatusFAHRSTUHL: str
