from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class PlannedMaintenance(BaseModel):
    status: str
    since: int
    until: int
    description: str


class TransportDevice(BaseModel):
    description: str
    identifier: str
    lastUpdate: Optional[int]
    name: str
    status: str
    type: str
    xcoordinate: int
    ycoordinate: int
    planned: Optional[PlannedMaintenance]


class StationTransportDevices(BaseModel):
    efaId: int
    name: str
    transportDevices: List[TransportDevice]
    aggregatedStatusROLLTREPPE: str
    aggregatedStatusFAHRSTUHL: str
