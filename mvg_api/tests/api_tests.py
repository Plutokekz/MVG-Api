import asyncio
import datetime
from typing import List

from mvg_api.api.api import Api, AsyncApi
from mvg_api.mvg import LocationNotFound
from mvg_api.models.route import LocationList, LocationType, Connections
from mvg_api.models.ticker import TickerList, SlimList


def test_get_ticker():
    api = Api()
    response = api.get_ticker()
    assert isinstance(response, TickerList)


def test_get_current_date():
    api = Api()
    response = api.get_current_date()
    assert isinstance(response, datetime.datetime)


def test_get_station_global_ids():
    api = Api()
    response = api.get_station_global_ids()
    assert isinstance(response, List)
    assert len(response) > 0


def test_get_slim():
    api = Api()
    response = api.get_slim()
    assert isinstance(response, SlimList)


def test_get_route():
    api = Api()
    response = api.get_route(
        "de:09162:6",
        "de:09162:50",
        sap_tickets=True,
        _time=datetime.datetime.now(),
        transport_type_call_taxi=True,
        max_walk_time_to_dest=5,
        max_walk_time_to_start=5,
        change_limit=3,
    )
    assert isinstance(response, Connections)


def test_get_location():
    api = Api()
    response = api.get_location("Marienplatz")
    assert isinstance(response, LocationList)
    for location in response.locations:
        if location.type == LocationType.STATION:
            if location.name == "Marienplatz":
                return
    raise LocationNotFound("Loaction Marienplatz not foudn in LocationList")


def test_get_ticker_async():
    api = AsyncApi()
    response = asyncio.run(api.get_ticker())
    assert isinstance(response, TickerList)


def test_get_current_date_async():
    api = AsyncApi()
    response = asyncio.run(api.get_current_date())
    assert isinstance(response, datetime.datetime)


def test_get_station_global_ids_async():
    api = AsyncApi()
    response = asyncio.run(api.get_station_global_ids())
    assert isinstance(response, List)
    assert len(response) > 0


def test_get_slim_async():
    api = AsyncApi()
    response = asyncio.run(api.get_slim())
    assert isinstance(response, SlimList)


def test_get_route_async():
    api = AsyncApi()
    response = asyncio.run(
        api.get_route(
            "de:09162:6",
            "de:09162:50",
            sap_tickets=True,
            _time=datetime.datetime.now(),
            transport_type_call_taxi=True,
            max_walk_time_to_dest=5,
            max_walk_time_to_start=5,
            change_limit=3,
        )
    )
    assert isinstance(response, Connections)


def test_get_location_async():
    api = AsyncApi()
    response = asyncio.run(api.get_location("Marienplatz"))
    assert isinstance(response, LocationList)
    for location in response.locations:
        if location.type == LocationType.STATION:
            if location.name == "Marienplatz":
                return
    raise LocationNotFound("Loaction Marienplatz not foudn in LocationList")
