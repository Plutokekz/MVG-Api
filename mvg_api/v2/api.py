import json
from typing import Dict, Any, Optional, List

import httpx

from mvg_api.v2.schemas import (
    ems,
    station,
    transportdevice,
    aushang,
)
from mvg_api.v2.schemas.location import LocationType


class RequestFailed(Exception):
    pass


class MVGRequests:
    url: str = "https://www.mvg.de/"

    @staticmethod
    def ticker(headers: Dict[str, str]) -> httpx.Request:
        return httpx.Request(
            "GET", f"{MVGRequests.url}api/ems/tickers", headers=headers
        )

    @staticmethod
    def station(station_id: str, headers: Dict[str, str]) -> httpx.Request:
        return httpx.Request(
            "GET", f"{MVGRequests.url}.rest/zdm/stations/{station_id}", headers=headers
        )

    @staticmethod
    def escalators_and_elevators(efa_id: int, headers: Dict[str, str]) -> httpx.Request:
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}.rest/mvgZoom/api/stations/{efa_id}",
            headers=headers,
        )

    @staticmethod
    def aushang(plan_id: str, headers: Dict[str, str]) -> httpx.Request:
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}.rest/aushang/stations",
            headers=headers,
            params={"id": plan_id},
        )

    @staticmethod
    def station_ids(headers: Dict[str, str]) -> httpx.Request:
        return httpx.Request(
            "GET", f"{MVGRequests.url}.rest/zdm/mvgStationGlobalIds", headers=headers
        )

    @staticmethod
    def location(
        query: str,
        limit_address_poi: int,
        limit_stations: int,
        location_types: List[LocationType],
        headers: Dict[str, str],
    ) -> httpx.Request:
        param = httpx.QueryParams(
            {
                "query": query,
                "limitAddressPoi": limit_address_poi,
                "limitStations": limit_stations,
                "locationTypes": (
                    ",".join([x.value for x in location_types])
                    if location_types is not None
                    else None
                ),
            }
        )
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/fib/v2/location",
            params=param,
            headers=headers,
        )

    @staticmethod
    def messages(headers: Dict[str, str], message_type=Optional[str]) -> httpx.Request:
        param = httpx.QueryParams({"messageType": message_type})
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/fib/v2/message",
            params=param,
            headers=headers,
        )

    @staticmethod
    def connection(
        origin_station_id: str,
        destination_station_id: str,
        routing_date_time: str,
        headers: Dict[str, str],
        *,
        routing_date_time_is_arrival: bool,
        transport_types: Optional[str] = None,
        origin_latitude: Optional[float] = None,
        origin_longitude: Optional[float] = None,
        destination_latitude: Optional[float] = None,
        destination_longitude: Optional[float] = None,
    ) -> httpx.Request:
        param = httpx.QueryParams(
            {
                "originStationGlobalId": origin_station_id,
                "destinationStationGlobalId": destination_station_id,
                "routingDateTime": routing_date_time,
                "routingDateTimeIsArrival": routing_date_time_is_arrival,
                "transportTypes": transport_types,
                "originLatitude": origin_latitude,
                "originLongitude": origin_longitude,
                "destinationLatitude": destination_latitude,
                "destinationLongitude": destination_longitude,
            }
        )
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/fib/v2/connection",
            params=param,
            headers=headers,
        )

    @staticmethod
    def lineinfo(headers: Dict[str, str], language: Optional[str]) -> httpx.Request:
        return httpx.Request(
            "GET", f"{MVGRequests.url}api/fib/v2/lineinfo/{language}", headers=headers
        )

    @staticmethod
    def stations(
        headers: Dict[str, str], hash_: Optional[str], world: Optional[bool]
    ) -> httpx.Request:
        param = httpx.QueryParams({"hash": hash_, "world": world})
        return httpx.Request(
            "GET", f"{MVGRequests.url}api/fib/v2/station", headers=headers, params=param
        )

    @staticmethod
    def lines(headers: Dict[str, str]):
        return httpx.Request(
            "GET", f"{MVGRequests.url}api/fib/v2/line", headers=headers
        )

    @staticmethod
    def zoom_station(div_id: int, headers: Dict[str, str]) -> httpx.Request:
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/fib/v2/mvgzoomstation/{div_id}",
            headers=headers,
        )

    @staticmethod
    def plan(div_id: int, headers: Dict[str, str]) -> httpx.Request:
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/fib/v2/mvgzoomstation/{div_id}/map",
            headers=headers,
        )

    @staticmethod
    def zoom_station_out_of_order(
        div_id: int, headers: Dict[str, str]
    ) -> httpx.Request:
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/fib/v2/mvgzoomstation/{div_id}/outoforder",
            headers=headers,
        )

    @staticmethod
    def vehicle(
        bbswlat: float,
        bbswlng: float,
        bbnelat: float,
        bbnelng: float,
        headers: Dict[str, str],
    ) -> httpx.Request:
        param = httpx.QueryParams(
            {
                "bbswlat": bbswlat,
                "bbswlng": bbswlng,
                "bbnelat": bbnelat,
                "bbnelng": bbnelng,
            }
        )
        return httpx.Request(
            "GET", f"{MVGRequests.url}api/fib/v2/vehicle", params=param, headers=headers
        )

    @staticmethod
    def surrounding_plan(
        plan_id: str,
        headers: Dict[str, str],
        world: bool = True,
        include_image_data: bool = True,
    ) -> httpx.Request:
        url = f"{MVGRequests.url}api/fib/v2/surroundingplan/{plan_id}"
        params = {"world": world, "includeImageData": include_image_data}
        return httpx.Request("GET", url, params=params, headers=headers)

    @staticmethod
    def surrounding_plans(
        headers: Dict[str, str], world: Optional[bool] = True
    ) -> httpx.Request:
        params = {"world": world}
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/fib/v2/surroundingplan",
            params=params,
            headers=headers,
        )


class SyncApi:
    __slots__ = ("client", "headers")

    client: httpx.Client
    headers: Dict[str, str]
    url: str = "https://www.mvg.de/"

    def __init__(self, client: httpx.Client = None):
        self.client = client if client is not None else httpx.Client()
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "sec-gpc": "1",
        }

    def _send_request(self, request: httpx.Request) -> Any:
        response = self.client.send(request)
        if response.status_code != 200:
            raise RequestFailed(
                f"Request failed with status code: {response.status_code} and response {response.text}"
            )
        try:
            return response.json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            return response.content

    def get_ticker(self) -> ems.Messages:
        """
        Get ticker messages, updates about the disruptions and planed works on the MVG train network
        There 2 types of messages DISRUPTION and PLANNED
        :return: a list es messages
        """
        response = self._send_request(MVGRequests.ticker(self.headers))
        return ems.Messages(response)

    def get_station(self, station_id: str) -> station.Station:
        """
        Get a station by its id the Station id can be found in the get_all_stations list, or it can be obtained from a
        location method wenn the found Location is of the type STATION
        :param station_id: for example de:09162:6 for Hauptbahnhof
        :return: a Station
        """
        response = self._send_request(MVGRequests.station(station_id, self.headers))
        return station.Station(**response)

    def get_escalators_and_elevators(
        self, efa_id: int
    ) -> transportdevice.StationTransportDevices:
        """
        Get the escalators and elevators location and status for a station
        :param efa_id: an integer number that is associated with a station. It is included in the Station object but
        under the name of divId for some reason.
        :return: a StationTransportDevices object
        """
        response = self._send_request(
            MVGRequests.escalators_and_elevators(efa_id, self.headers)
        )
        return transportdevice.StationTransportDevices(**response)

    def get_aushang(self, plan_id: str) -> aushang.Aushaenge:
        """
        Get the aushang for a station, get all Playn that a currently active in a stations blackboard.
        :param plan_id: I am not sure bit it seems to be the first 2 letters of the station name in uppercase.
         For example KA for Karlsplatz
        :return: a list of aushaenge
        """
        response = self._send_request(MVGRequests.aushang(plan_id, self.headers))
        return aushang.Aushaenge(response)

    def get_station_ids(self) -> List[str]:
        """
        Get all the station ids
        :return: returns a list of strings with all the station ids that are available
        """
        response = self._send_request(MVGRequests.station_ids(self.headers))
        return list(response)


class AsyncApi:
    __slots__ = ("client", "headers")

    client: httpx.AsyncClient
    headers: Dict[str, str]
    url: str = "https://www.mvg.de/"

    def __init__(self, client: httpx.Client = None):
        self.client = client if client is not None else httpx.AsyncClient()
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "sec-gpc": "1",
        }

    async def _send_request(self, request: httpx.Request) -> Any:
        response = await self.client.send(request)
        if response.status_code != 200:
            raise RequestFailed(
                f"Request failed with status code: {response.status_code} and response {response.text}"
            )
        try:
            return response.json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            return response.content

    async def get_ticker(self) -> ems.Messages:
        """
        Get ticker messages, updates about the disruptions and planed works on the MVG train network
        There 2 types of messages DISRUPTION and PLANNED
        :return: a list es messages
        """
        response = await self._send_request(MVGRequests.ticker(self.headers))
        return ems.Messages(response)

    async def get_station(self, station_id: str) -> station.Station:
        """
        Get a station by its id the Station id can be found in the get_all_stations list, or it can be obtained from a
        location method wenn the found Location is of the type STATION
        :param station_id: for example de:09162:6 for Hauptbahnhof
        :return: a Station
        """
        response = await self._send_request(
            MVGRequests.station(station_id, self.headers)
        )
        return station.Station(**response)

    async def get_escalators_and_elevators(
        self, efa_id: int
    ) -> transportdevice.StationTransportDevices:
        """
        Get the escalators and elevators location and status for a station
        :param efa_id: an integer number that is associated with a station. It is included in the Station object but
        under the name of divId for some reason.
        :return: a StationTransportDevices object
        """
        response = await self._send_request(
            MVGRequests.escalators_and_elevators(efa_id, self.headers)
        )
        return transportdevice.StationTransportDevices(**response)

    async def get_aushang(self, plan_id: str) -> aushang.Aushaenge:
        """
        Get the aushang for a station, get all Playn that a currently active in a stations blackboard.
        :param plan_id: I am not sure bit it seems to be the first 2 letters of the station name in uppercase.
         For example
        KA for Karlsplatz
        :return: a list of aushaenge
        """
        response = await self._send_request(MVGRequests.aushang(plan_id, self.headers))
        return aushang.Aushaenge(response)

    async def get_station_ids(self) -> List[str]:
        """
        Get all the station ids
        :return: returns a list of strings with all the station ids that are available
        """
        response = await self._send_request(MVGRequests.station_ids(self.headers))
        return list(response)
