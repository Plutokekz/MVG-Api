from __future__ import annotations

from pydantic import BaseModel


class StationOutOfOrder(BaseModel):
    stationDivaId: int
    hasZoomData: bool
    hasOutOfOrderEscalator: bool
    hasOutOfOrderElevator: bool
