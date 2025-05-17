import asyncio

from mvg_api.v2.api import SyncApi, AsyncApi
from mvg_api.v2.schemas.ems import Messages


def test_get_ticker():
    api = SyncApi()
    result = api.get_ticker()
    assert isinstance(result, Messages)


def test_get_station():
    api = SyncApi()
    result = api.get_station("de:09162:6")
    assert result.id == "de:09162:6"
    assert result.name == "Hauptbahnhof Bahnhofsplatz"


def test_get_escalators_and_elevators():
    api = SyncApi()
    result = api.get_escalators_and_elevators(6)
    assert result.efaId == 6
    assert result.name == "Hauptbahnhof"


def test_get_aushang():
    api = SyncApi()
    result = api.get_aushang("KA")
    assert len(result) != 0


def test_get_station_ids():
    api = SyncApi()
    result = api.get_station_ids()
    assert len(result) != 0
    assert isinstance(result[0], str)


def test_get_ticker_async():
    api = AsyncApi()
    result = asyncio.run(api.get_ticker())
    assert isinstance(result, Messages)


def test_get_station_async():
    api = AsyncApi()
    result = asyncio.run(api.get_station("de:09162:6"))
    assert result.id == "de:09162:6"
    assert result.name == "Hauptbahnhof Bahnhofsplatz"


def test_get_escalators_and_elevators_async():
    api = AsyncApi()
    result = asyncio.run(api.get_escalators_and_elevators(6))
    assert result.efaId == 6
    assert result.name == "Hauptbahnhof"


def test_get_aushang_async():
    api = AsyncApi()
    result = asyncio.run(api.get_aushang("KA"))
    assert len(result) != 0


def test_get_station_ids_async():
    api = AsyncApi()
    result = asyncio.run(api.get_station_ids())
    assert len(result) != 0
    assert isinstance(result[0], str)
