from typing import Any, List
import datetime

import httpx
from mvg_api.v1.schemas.ticker import TickerList, SlimList
from mvg_api.v1.schemas.route import Connections, LocationList


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

    def get_slim(self) -> SlimList:
        """
        A small version of the ticker, the model for the endpoint is not implemented
        :return:
        """
        response = self._send_request("api/ems/slim")
        return SlimList(__root__=response)

    def get_route(
        self,
        origin_station_global_id: str,
        destination_station_global_id: str,
        routing_date_time: datetime.datetime | None = None,
        routing_date_time_is_arrival: bool = False,
        transport_types: str = "SCHIFF,RUFTAXI,BAHN,UBAHN,TRAM,SBAHN,BUS,REGIONAL_BUS",
    ):
        """
        Get all available routes from one destination to another
        :return:
        """
        if routing_date_time is None:
            routing_date_time = self.get_current_date()
            routing_date_time = routing_date_time.strftime("%Y-%m-%dT%H:%M:%S.000%zZ")

        args = (
            f"?originStationGlobalId={origin_station_global_id}"
            f"&destinationStationGlobalId={destination_station_global_id}"
            f"&transportTypes={transport_types}"
            f"&routingDateTime={routing_date_time}"
            f"&routingDateTimeIsArrival={str(routing_date_time_is_arrival).lower()}"
        )
        response = self._send_request("api/fib/v2/connection" + args)
        return Connections(connectionList=response)

    def get_location(self, name: str):
        """
        Get a list of locations by name
        :param name: name of the location / Station
        :return: a list of Locations
        """
        response = self._send_request(f"api/fib/v2/location?query={name}")
        return LocationList(locations=response)


class AsyncApi:
    __slots__ = ("client",)

    client: httpx.AsyncClient
    url: str = "https://www.mvg.de/"

    def __init__(self, client: httpx.AsyncClient = None):
        self.client = client if client is not None else httpx.AsyncClient()

    async def _send_request(self, endpoint) -> Any:
        headers = {
            "accept": "application/json, text/plain, */*",
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

    async def get_slim(self) -> SlimList:
        """
        A small version of the ticker, the model for the endpoint is not implemented
        :return:
        """
        response = await self._send_request("api/ems/slim")
        return SlimList(__root__=response)

    async def get_route(
        self,
        origin_station_global_id: str,
        destination_station_global_id: str,
        routing_date_time: datetime.datetime | None = None,
        routing_date_time_is_arrival: bool = False,
        transport_types: str = "SCHIFF,RUFTAXI,BAHN,UBAHN,TRAM,SBAHN,BUS,REGIONAL_BUS",
    ):
        """
        Get all available routes from one destination to another
        :return:
        """
        if routing_date_time is None:
            routing_date_time = await self.get_current_date()
            routing_date_time = routing_date_time.strftime("%Y-%m-%dT%H:%M:%S.000%zZ")

        args = (
            f"?originStationGlobalId={origin_station_global_id}"
            f"&destinationStationGlobalId={destination_station_global_id}"
            f"&transportTypes={transport_types}"
            f"&routingDateTime={routing_date_time}"
            f"&routingDateTimeIsArrival={str(routing_date_time_is_arrival).lower()}"
        )
        response = await self._send_request("api/fib/v2/connection" + args)
        return Connections(connectionList=response)

    async def get_location(self, name: str):
        """
        Get a list of locations by name
        :param name: name of the location / Station
        :return: a list of Locations
        """
        response = await self._send_request(f"api/fib/v2/location?query={name}")
        return LocationList(locations=response)
