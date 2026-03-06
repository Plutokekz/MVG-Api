import datetime

from mvg_api.v3.schemas import (
    aushang,
    connection,
    departure,
    line,
    location,
    messages,
    nearby,
    station,
    # stations,
    ticker,
    ubahn_map,
    zoom,
)
from mvg_api.v3.syncapi import SyncApi


def test_get_aushang():
    api = SyncApi()
    result = api.get_aushang("SE")
    assert isinstance(result, aushang.Aushaenge)
    assert len(result) > 0


def test_get_connections_stationids():
    api = SyncApi()
    result = api.get_connections(
        "de:09162:50",
        "de:09162:40",
        routing_date_time=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.") + "000Z"
    )
    assert isinstance(result, connection.Connections)
    assert len(result) > 0


def test_get_departures():
    api = SyncApi()
    result = api.get_departures("de:09162:50", limit=1)
    assert isinstance(result, departure.Departures)
    assert len(result) == 1


def test_get_lines():
    api = SyncApi()
    result = api.get_lines()
    assert isinstance(result, line.Lines)
    assert len(result) > 1


def test_get_locations():
    api = SyncApi()
    result = api.get_locations(query="Sendlinger Tor")
    assert isinstance(result, location.Locations)
    assert len(result) > 0


def test_get_messages():
    api = SyncApi()
    result = api.get_messages()
    assert isinstance(result, messages.Messages)
    assert len(result) > 0


def test_get_nearby():
    api = SyncApi()
    result = api.get_nearby(48.1334, 11.5667)
    assert isinstance(result, nearby.Stations)
    assert len(result) > 0


def test_get_station_ids():
    api = SyncApi()
    result = api.get_station_ids()
    assert isinstance(result[0], str)
    assert len(result) > 0


def test_get_station():
    api = SyncApi()
    result = api.get_station("de:09162:50")
    assert isinstance(result, station.Station)
    assert result.id == "de:09162:50"
    assert result.name == "Sendlinger Tor"


def test_get_stations():
    pass
    # skip beca<use endpoint loads quite a lot of data
    # api = SyncApi()
    # result = api.get_stations()
    # assert isinstance(result, stations.Stations)
    # assert len(result) > 0


def test_get_ticker():
    api = SyncApi()
    result = api.get_ticker()
    assert isinstance(result, ticker.Messages)
    assert len(result) > 0


def test_get_ubahn_map():
    api = SyncApi()
    result = api.get_ubahn_map()
    assert isinstance(result, ubahn_map.UbahnMap)
    assert len(result) > 0


def test_get_zoom_single():
    api = SyncApi()
    result = api.get_zoom(50)
    assert isinstance(result, zoom.ZoomStation)
    assert result.efaId == 50
    assert result.name == "Sendlinger Tor"


def test_get_zoom_all():
    api = SyncApi()
    result = api.get_zoom()
    assert isinstance(result, zoom.ZoomStations)
    assert len(result) > 1


def test_find_location():
    api = SyncApi()
    result = api.find_location("Sendlinger Tor")
    assert isinstance(result, location.Location)
    assert result.name == "Sendlinger Tor"

def test_find_location_station():
    # difficult to test station only type
    api = SyncApi()
    result = api.find_location_station("Sendlinger Tor")
    assert isinstance(result, location.Location)
    assert result.type == location.LocationType.STATION
    assert result.name == "Sendlinger Tor"
