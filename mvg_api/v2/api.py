import json
from typing import Dict, Any, Optional, List

import httpx

from mvg_api.v2.schemas import (
    ems,
    station,
    departure,
    transportdevice,
    aushang,
    zoom_station,
    stations,
    location,
    line,
    lineinfo,
    connection,
    vehicel,
    surounding_plans,
    messages,
    out_of_order,
)


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
    def departures(
        station_id: str,
        headers: Dict[str, str],
        *,
        limit: Optional[int] = None,
        offset_minutes: Optional[int] = None,
        transport_types: Optional[Any] = None,
        language: Optional[str] = None,
    ) -> httpx.Request:
        param = httpx.QueryParams(
            {
                "globalId": station_id,
                "limit": limit,
                "offsetInMinutes": offset_minutes,
                "transportTypes": transport_types,
                "language": language,
            }
        )
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/fib/v2/departure",
            params=param,
            headers=headers,
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
        location_types: List[str],
        headers: Dict[str, str],
    ) -> httpx.Request:
        param = httpx.QueryParams(
            {
                "query": query,
                "limitAddressPoi": limit_address_poi,
                "limitStations": limit_stations,
                "locationTypes": location_types,
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


class Api:
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
        except json.JSONDecodeError:
            return response.content

    def get_ticker(self) -> ems.Messages:
        response = self._send_request(MVGRequests.ticker(self.headers))
        return ems.Messages(__root__=response)

    def get_station(self, station_id: str) -> station.Station:
        response = self._send_request(MVGRequests.station(station_id, self.headers))
        return station.Station(**response)

    def departures(
        self,
        station_id: str,
        *,
        limit: Optional[int] = None,
        offset_minutes: Optional[int] = None,
        transport_types: Optional[Any] = None,
        language: Optional[str] = None,
    ) -> departure.Departures:
        response = self._send_request(
            MVGRequests.departures(
                station_id,
                self.headers,
                limit=limit,
                offset_minutes=offset_minutes,
                transport_types=transport_types,
                language=language,
            )
        )
        return departure.Departures(__root__=response)

    def get_escalators_and_elevators(
        self, efa_id: int
    ) -> transportdevice.StationTransportDevices:
        response = self._send_request(
            MVGRequests.escalators_and_elevators(efa_id, self.headers)
        )
        return transportdevice.StationTransportDevices(**response)

    def get_aushang(self, plan_id: str) -> aushang.Aushaenge:
        response = self._send_request(MVGRequests.aushang(plan_id, self.headers))
        return aushang.Aushaenge(__root__=response)

    def get_station_ids(self) -> List[str]:
        response = self._send_request(MVGRequests.station_ids(self.headers))
        return list(response)

    def get_location(
        self,
        query: str,
        limit_address_poi: Optional[int] = None,
        limit_stations: Optional[int] = None,
        location_types: Optional[List[str]] = None,
    ) -> location.Locations:
        response = self._send_request(
            MVGRequests.location(
                query, limit_address_poi, limit_stations, location_types, self.headers
            )
        )
        return location.Locations(__root__=response)

    def get_messages(self, message_type=Optional[str]) -> messages.Messages:
        response = self._send_request(MVGRequests.messages(self.headers, message_type))
        return messages.Messages(__root__=response)

    def get_connection(
        self,
        origin_station_id: str,
        destination_station_id: str,
        routing_date_time: str,
        *,
        routing_date_time_is_arrival: bool,
        transport_types: Optional[str] = None,
        origin_latitude: Optional[float] = None,
        origin_longitude: Optional[float] = None,
        destination_latitude: Optional[float] = None,
        destination_longitude: Optional[float] = None,
    ) -> connection.Connections:
        response = self._send_request(
            MVGRequests.connection(
                origin_station_id,
                destination_station_id,
                routing_date_time,
                self.headers,
                routing_date_time_is_arrival=routing_date_time_is_arrival,
                transport_types=transport_types,
                origin_latitude=origin_latitude,
                origin_longitude=origin_longitude,
                destination_latitude=destination_latitude,
                destination_longitude=destination_longitude,
            )
        )
        return connection.Connections(__root__=response)

    def get_lineinfo(self, language: Optional[str]) -> lineinfo.Infos:
        response = self._send_request(MVGRequests.lineinfo(self.headers, language))
        return lineinfo.Infos(__root__=response)

    def get_stations(
        self, hash_: Optional[str] = None, world: Optional[bool] = None
    ) -> stations.Locations:
        response = self._send_request(MVGRequests.stations(self.headers, hash_, world))
        return stations.Locations(**response)

    def get_lines(self) -> line.Lines:
        response = self._send_request(MVGRequests.lines(self.headers))
        return line.Lines(__root__=response)

    def get_zoom_station(self, div_id: int) -> zoom_station.ZoomStation:
        response = self._send_request(MVGRequests.zoom_station(div_id, self.headers))
        return zoom_station.ZoomStation(**response)

    def get_plan(self, div_id: int) -> bytes:
        response = self._send_request(MVGRequests.plan(div_id, self.headers))
        return bytes(response)

    def get_zoom_station_out_of_order(
        self, div_id: int
    ) -> out_of_order.StationOutOfOrder:
        response = self._send_request(
            MVGRequests.zoom_station_out_of_order(div_id, self.headers)
        )
        return out_of_order.StationOutOfOrder(**response)

    def get_vehicles_in_bounding_box(
        self, bbswlat: float, bbswlng: float, bbnelat: float, bbnelng: float
    ) -> vehicel.VehiclesAndSharingStations:
        response = self._send_request(
            MVGRequests.vehicle(bbswlat, bbswlng, bbnelat, bbnelng, self.headers)
        )
        return vehicel.VehiclesAndSharingStations(**response)

    def get_surrounding_plan(
        self, plan_id: str, world: bool = True, include_image_data: bool = True
    ) -> surounding_plans.Plan:
        response = self._send_request(
            MVGRequests.surrounding_plan(
                plan_id, self.headers, world, include_image_data
            )
        )
        return surounding_plans.Plan(**response)

    def get_surrounding_plans(
        self, world: Optional[bool] = True
    ) -> surounding_plans.Plans:
        response = self._send_request(
            MVGRequests.surrounding_plans(self.headers, world)
        )
        return surounding_plans.Plans(__root__=response)
