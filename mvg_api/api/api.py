from typing import Any, Tuple, List
import time
import datetime

import httpx
from mvg_api.models.ticker import TickerList, Station, SlimList
from mvg_api.models.route import Connections, LocationList


class RequestFailed(Exception):
    pass


class Api:
    __slots__ = ("client",)

    client: httpx.Client
    url: str = "https://www.mvg.de/"

    def __init__(self, client: httpx.Client = None):
        self.client = client if client is not None else httpx.Client()

    def _send_request(self, endpoint) -> Any:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "de-DE,de;q=0.8",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-gpc": "1",
        }
        response = self.client.get(self.url + endpoint, headers=headers)
        if response.status_code != 200:
            raise RequestFailed(
                f"Request failed with status code: {response.status_code} and response {response.text}"
            )
        return response.json()

    def get_ticker(self) -> TickerList:
        """
        Get all disruption or service work form the current departures
        :return:
        """
        response = self._send_request("api/ems/tickers")
        return TickerList(__root__=response)

    def get_current_date(self) -> datetime.datetime:
        """
        Get the current date with time from MVG
        :return:
        """
        response = self._send_request("clockService/currentDate")
        timestamp = float(response) / 1000
        return datetime.datetime.fromtimestamp(timestamp)

    def get_station_global_ids(self) -> List[str]:
        """
        Get a list of the global station id's
        :return: list of station id's
        """
        response = self._send_request(".rest/zdm/mvgStationGlobalIds")
        return list(response)

    def get_slim(self) -> Any:
        """
        A small version of the ticker, the model for the endpoint is not implemented
        :return:
        """
        response = self._send_request("api/ems/slim")
        return SlimList(__root__=response)

    def get_route(
        self,
        station_from: str | Tuple[float, float],
        station_to: str | Tuple[float, float],
        *,
        _time: datetime.datetime = None,
        sap_tickets: bool = False,
        transport_type_call_taxi: bool = False,
        arrival_time: bool = False,
        max_walk_time_to_start: int = None,
        max_walk_time_to_dest: int = None,
        change_limit: int = None,
        ubahn: bool = True,
        bus: bool = True,
        tram: bool = True,
        sbahn: bool = True,
    ):
        """
        Get all available routes from one destination to another
        :param station_from: id from station
        :param station_to: id from station
        :param _time: departure time
        :param sap_tickets: also return the available tickets for the rout
        :param transport_type_call_taxi: allow taxies in the rout
        :param arrival_time: make the departure timer the arrival time
        :param max_walk_time_to_start: max walking time to departure destination in minutes
        :param max_walk_time_to_dest: max walking time to arrival destination in minutes
        :param change_limit: max changes
        :param ubahn: use ubahn in rout
        :param bus: use bus in rout
        :param tram: use tram in rout
        :param sbahn: use sbahn in rout
        :return:
        """

        args = "?"
        if isinstance(station_from, Tuple):
            args += f"fromLatitude={station_from[0]}&fromLongitude={station_from[1]}"
        else:
            Station.valid_id(_id=station_from)
            args += f"fromStation={station_from}"
        if isinstance(station_to, Tuple):
            args += f"toLatitude={station_to[0]}&toLongitude={station_to[1]}"
        else:
            Station.valid_id(_id=station_to)
            args += f"&toStation={station_to}"
        if _time is not None:
            args += f"&time={int(time.mktime(_time.timetuple()) * 1000)}"
        if sap_tickets is not None:
            args += f"&sapTickets={str(sap_tickets).lower()}"
        if transport_type_call_taxi is not None:
            args += f"&transportTypeCallTaxi={str(transport_type_call_taxi).lower()}"
        if arrival_time is not None:
            args += f"&arrival={str(arrival_time).lower()}"
        if max_walk_time_to_start is not None:
            args += f"&maxTravelTimeFootwayToStation={max_walk_time_to_start}"
        if max_walk_time_to_dest is not None:
            args += f"&maxTravelTimeFootwayToDestination={max_walk_time_to_dest}"
        if change_limit is not None:
            args += f"&changeLimit={change_limit}"
        if ubahn is not None:
            args += f"&transportTypeUnderground={str(ubahn).lower()}"
        if bus is not None:
            args += f"&transportTypeBus={str(bus).lower()}"
        if tram is not None:
            args += f"&transportTypeTram={str(tram).lower()}"
        if sbahn is not None:
            args += f"&transportTypeSBahn={str(sbahn).lower()}"
        response = self._send_request("api/fahrinfo/routing/" + args)
        return Connections(**response)

    def get_location(self, name: str):
        """
        Get a list of locations by name
        :param name: name of the location / Station
        :return: a list of Locations
        """
        response = self._send_request(f"api/fahrinfo/location/queryWeb?q={name}")
        return LocationList(**response)


class AsyncApi:
    __slots__ = ("client",)

    client: httpx.AsyncClient
    url: str = "https://www.mvg.de/"

    def __init__(self, client: httpx.AsyncClient = None):
        self.client = client if client is not None else httpx.AsyncClient()

    async def _send_request(self, endpoint) -> Any:
        headers = {
            "accept": "application/json",
            "accept-language": "de-DE,de;q=0.8",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-gpc": "1",
        }
        response = await self.client.get(self.url + endpoint, headers=headers)
        if response.status_code != 200:
            raise RequestFailed(
                f"Request failed with status code: {response.status_code} and response {response.text}"
            )
        return response.json()

    async def get_ticker(self) -> TickerList:
        """
        Get all disruption or service work form the current departures
        :return:
        """
        response = await self._send_request("api/ems/tickers")
        return TickerList(__root__=response)

    async def get_current_date(self) -> datetime.datetime:
        """
        Get the current date with time from MVG
        :return:
        """
        response = await self._send_request("clockService/currentDate")
        timestamp = float(response) / 1000
        return datetime.datetime.fromtimestamp(timestamp)

    async def get_station_global_ids(self) -> List[str]:
        """
        Get a list of the global station id's
        :return: list of station id's
        """
        response = await self._send_request(".rest/zdm/mvgStationGlobalIds")
        return list(response)

    async def get_slim(self) -> Any:
        """
        A small version of the ticker, the model for the endpoint is not implemented
        :return:
        """
        return await self._send_request("api/ems/slim")

    async def get_route(
        self,
        station_from: str | Tuple[float, float],
        station_to: str | Tuple[float, float],
        *,
        _time: datetime.datetime = None,
        sap_tickets: bool = False,
        transport_type_call_taxi: bool = False,
        arrival_time: bool = False,
        max_walk_time_to_start: int = None,
        max_walk_time_to_dest: int = None,
        change_limit: int = None,
        ubahn: bool = True,
        bus: bool = True,
        tram: bool = True,
        sbahn: bool = True,
    ):
        """
        Get all available routes from one destination to another
        :param station_from: id from station
        :param station_to: id from station
        :param _time: departure time
        :param sap_tickets: also return the available tickets for the rout
        :param transport_type_call_taxi: allow taxies in the rout
        :param arrival_time: make the departure timer the arrival time
        :param max_walk_time_to_start: max walking time to departure destination in minutes
        :param max_walk_time_to_dest: max walking time to arrival destination in minutes
        :param change_limit: max changes
        :param ubahn: use ubahn in rout
        :param bus: use bus in rout
        :param tram: use tram in rout
        :param sbahn: use sbahn in rout
        :return:
        """

        args = "?"
        if isinstance(station_from, Tuple):
            args += f"fromLatitude={station_from[0]}&fromLongitude={station_from[1]}"
        else:
            Station.valid_id(_id=station_from)
            args += f"fromStation={station_from}"
        if isinstance(station_to, Tuple):
            args += f"toLatitude={station_to[0]}&toLongitude={station_to[1]}"
        else:
            Station.valid_id(_id=station_to)
            args += f"&toStation={station_to}"
        if _time is not None:
            args += f"&time={int(time.mktime(_time.timetuple()) * 1000)}"
        if sap_tickets is not None:
            args += f"&sapTickets={str(sap_tickets).lower()}"
        if transport_type_call_taxi is not None:
            args += f"&transportTypeCallTaxi={str(transport_type_call_taxi).lower()}"
        if arrival_time is not None:
            args += f"&arrival={str(arrival_time).lower()}"
        if max_walk_time_to_start is not None:
            args += f"&maxTravelTimeFootwayToStation={max_walk_time_to_start}"
        if max_walk_time_to_dest is not None:
            args += f"&maxTravelTimeFootwayToDestination={max_walk_time_to_dest}"
        if change_limit is not None:
            args += f"&changeLimit={change_limit}"
        if ubahn is not None:
            args += f"&transportTypeUnderground={str(ubahn).lower()}"
        if bus is not None:
            args += f"&transportTypeBus={str(bus).lower()}"
        if tram is not None:
            args += f"&transportTypeTram={str(tram).lower()}"
        if sbahn is not None:
            args += f"&transportTypeSBahn={str(sbahn).lower()}"
        response = await self._send_request("api/fahrinfo/routing/" + args)
        return Connections(**response)

    async def get_location(self, name: str):
        """
        Get a list of locations by name
        :param name: name of the location / Station
        :return: a list of Locations
        """
        response = await self._send_request(f"api/fahrinfo/location/queryWeb?q={name}")
        return LocationList(**response)
