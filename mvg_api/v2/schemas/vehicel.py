from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Deeplinks(BaseModel):
    androidDeeplink: str
    iosDeeplink: str


class Vehicle(BaseModel):
    longitude: float
    latitude: float
    type: str
    deeplinks: Deeplinks
    externalId: str
    idForBooking: str
    idForReservation: str


class SharingStation(BaseModel):
    id: str
    name: str
    longitude: float
    latitude: float
    vehicleType: str
    vehicleCount: int
    deeplinks: Deeplinks


class VehiclesAndSharingStations(BaseModel):
    vehicles: List[Vehicle]
    sharingStations: List[SharingStation]
