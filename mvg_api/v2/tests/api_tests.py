import asyncio

from mvg_api.v2.api import SyncApi, AsyncApi
from mvg_api.v2.schemas import departure, location
from mvg_api.v2.schemas.connection import Connections
from mvg_api.v2.schemas.ems import Messages
from mvg_api.v2.schemas.line import Lines
from mvg_api.v2.schemas.lineinfo import Infos
from mvg_api.v2.schemas.stations import Locations
from mvg_api.v2.schemas.surounding_plans import Plan, BasePlan
from mvg_api.v2.schemas.messages import Message


def test_get_ticker():
    api = SyncApi()
    result = api.get_ticker()
    assert isinstance(result, Messages)


def test_get_station():
    api = SyncApi()
    result = api.get_station("de:09162:6")
    assert result.id == "de:09162:6"
    assert result.name == "Hauptbahnhof"


def test_departures():
    api = SyncApi()
    result = api.get_departures("de:09162:6", limit=1)
    assert isinstance(result, departure.Departures)
    assert len(result.__root__) == 1


def test_get_escalators_and_elevators():
    api = SyncApi()
    result = api.get_escalators_and_elevators(6)
    assert result.efaId == 6
    assert result.name == "Hauptbahnhof"


def test_get_aushang():
    api = SyncApi()
    result = api.get_aushang("KA")
    assert len(result.__root__) != 0


def test_get_station_ids():
    api = SyncApi()
    result = api.get_station_ids()
    assert len(result) != 0
    assert isinstance(result[0], str)


def test_get_location():
    api = SyncApi()
    result = api.get_location("Hauptbahnhof")
    assert len(result.__root__) != 0
    assert isinstance(result.__root__[0], location.Location)


def test_get_messages():
    api = SyncApi()
    result = api.get_messages()
    assert len(result.__root__) != 0
    assert isinstance(result.__root__[0], Message)


def test_get_connection():
    api = SyncApi()
    result = api.get_connection(
        "de:09162:1606",
        "de:09162:6",
        routing_date_time="2023-06-25T20:04:47.552Z",
        routing_date_time_is_arrival=False,
    )
    assert isinstance(result, Connections)


def test_get_lineinfo():
    api = SyncApi()
    result = api.get_lineinfo(language="GERMAN")
    assert isinstance(result, Infos)


def test_get_stations():
    api = SyncApi()
    result = api.get_stations()
    assert isinstance(result, Locations)


def test_get_lines():
    api = SyncApi()
    result = api.get_lines()
    assert isinstance(result, Lines)


def test_get_zoom_station():
    api = SyncApi()
    result = api.get_zoom_station(6)
    assert result.stationDivaId == 6
    assert result.name == "Hauptbahnhof"


def test_get_plan():
    api = SyncApi()
    result = api.get_plan(6)
    assert isinstance(result, bytes)


def test_get_zoom_station_out_of_order():
    api = SyncApi()
    result = api.get_zoom_station_out_of_order(6)
    assert result.stationDivaId == 6


def test_get_vehicles_in_bounding_box():
    api = SyncApi()
    result = api.get_vehicles_in_bounding_box(
        bbswlat=48.1154, bbswlng=11.5048, bbnelat=48.1409, bbnelng=11.5722
    )
    assert len(result.vehicles) != 0
    assert len(result.sharingStations) != 0


def test_get_surrounding_plan():
    api = SyncApi()
    result = api.get_surrounding_plan("KA")
    assert isinstance(result, Plan)
    assert result.planId == "KA"


def test_get_surrounding_plans():
    api = SyncApi()
    result = api.get_surrounding_plans()
    assert len(result.__root__) != 0
    assert isinstance(result.__root__[0], BasePlan)


def test_get_ticker_async():
    api = AsyncApi()
    result = asyncio.run(api.get_ticker())
    assert isinstance(result, Messages)


def test_get_station_async():
    api = AsyncApi()
    result = asyncio.run(api.get_station("de:09162:6"))
    assert result.id == "de:09162:6"
    assert result.name == "Hauptbahnhof"


def test_departures_async():
    api = AsyncApi()
    result = asyncio.run(api.get_departures("de:09162:6", limit=1))
    assert isinstance(result, departure.Departures)
    assert len(result.__root__) == 1


def test_get_escalators_and_elevators_async():
    api = AsyncApi()
    result = asyncio.run(api.get_escalators_and_elevators(6))
    assert result.efaId == 6
    assert result.name == "Hauptbahnhof"


def test_get_aushang_async():
    api = AsyncApi()
    result = asyncio.run(api.get_aushang("KA"))
    assert len(result.__root__) != 0


def test_get_station_ids_async():
    api = AsyncApi()
    result = asyncio.run(api.get_station_ids())
    assert len(result) != 0
    assert isinstance(result[0], str)


def test_get_location_async():
    api = AsyncApi()
    result = asyncio.run(api.get_location("Hauptbahnhof"))
    assert len(result.__root__) != 0
    assert isinstance(result.__root__[0], location.Location)


def test_get_messages_async():
    api = AsyncApi()
    result = asyncio.run(api.get_messages())
    assert len(result.__root__) != 0
    assert isinstance(result.__root__[0], Message)


def test_get_connection_async():
    api = AsyncApi()
    result = asyncio.run(
        api.get_connection(
            "de:09162:1606",
            "de:09162:6",
            routing_date_time="2023-06-25T20:04:47.552Z",
            routing_date_time_is_arrival=False,
        )
    )
    assert isinstance(result, Connections)


def test_get_lineinfo_async():
    api = AsyncApi()
    result = asyncio.run(api.get_lineinfo(language="GERMAN"))
    assert isinstance(result, Infos)


def test_get_stations_async():
    api = AsyncApi()
    result = asyncio.run(api.get_stations())
    assert isinstance(result, Locations)


def test_get_lines_async():
    api = AsyncApi()
    result = asyncio.run(api.get_lines())
    assert isinstance(result, Lines)


def test_get_zoom_station_async():
    api = AsyncApi()
    result = asyncio.run(api.get_zoom_station(6))
    assert result.stationDivaId == 6
    assert result.name == "Hauptbahnhof"


def test_get_plan_async():
    api = AsyncApi()
    result = asyncio.run(api.get_plan(6))
    assert isinstance(result, bytes)


def test_get_zoom_station_out_of_order_async():
    api = AsyncApi()
    result = asyncio.run(api.get_zoom_station_out_of_order(6))
    assert result.stationDivaId == 6


def test_get_vehicles_in_bounding_box_async():
    api = AsyncApi()
    result = asyncio.run(
        api.get_vehicles_in_bounding_box(
            bbswlat=48.1154, bbswlng=11.5048, bbnelat=48.1409, bbnelng=11.5722
        )
    )
    assert len(result.vehicles) != 0
    assert len(result.sharingStations) != 0


def test_get_surrounding_plan_async():
    api = AsyncApi()
    result = asyncio.run(api.get_surrounding_plan("KA"))
    assert isinstance(result, Plan)
    assert result.planId == "KA"


def test_get_surrounding_plans_async():
    api = AsyncApi()
    result = asyncio.run(api.get_surrounding_plans())
    assert len(result.__root__) != 0
    assert isinstance(result.__root__[0], BasePlan)
