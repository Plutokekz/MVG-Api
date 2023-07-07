from __future__ import annotations

from typing import List

from pydantic import BaseModel


class TransportDevice(BaseModel):
    status: str
    name: str
    identifier: str
    xcoordinate: int
    ycoordinate: int
    description: str
    type: str


class ZoomStation(BaseModel):
    stationDivaId: int
    name: str
    transportDevices: List[TransportDevice]
