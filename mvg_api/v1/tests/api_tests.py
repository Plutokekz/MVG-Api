import asyncio
import datetime
from typing import List

from mvg_api.v1.api import Api, AsyncApi
from mvg_api.v1.schemas.ticker import TickerList, SlimList


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
