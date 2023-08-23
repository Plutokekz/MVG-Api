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
        location_types: List[LocationType],
        headers: Dict[str, str],
    ) -> httpx.Request:
        param = httpx.QueryParams(
            {
                "query": query,
                "limitAddressPoi": limit_address_poi,
                "limitStations": limit_stations,
                "locationTypes": ",".join([x.value for x in location_types]) if location_types is not None else None,
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
        except json.JSONDecodeError:
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

    def get_departures(
        self,
        station_id: str,
        *,
        limit: Optional[int] = None,
        offset_minutes: Optional[int] = None,
        transport_types: Optional[Any] = None,
        language: Optional[str] = None,
    ) -> departure.Departures:
        """
        Get the departures for a station
        :param station_id: the same id as in get_station, for example de:09162:6 for Hauptbahnhof, and it can be
        obtained
        from a location method wenn the found Location is of the type STATION or from the get_all_stations method
        :param limit: the maximum number of departures to return
        :param offset_minutes: the offset in minutes from now for the departures
        :param transport_types: select specific transport types, available types are UBAHN,TRAM,BUS,SBAHN,SCHIFF
        :param language: the language ? I have no idea why this is here maybe for the language in the response. But I
        didn't see any difference when I changed it
        :return: a list of departures
        """
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
        return departure.Departures(response)

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

    def get_location(
        self,
        query: str,
        limit_address_poi: Optional[int] = None,
        limit_stations: Optional[int] = None,
        location_types: Optional[List[LocationType]] = None,
    ) -> location.Locations:
        """
        Get the location of a query, it can be a station name or a street name or a POI
        :param query: the Address or the station name or the POI name
        :param limit_address_poi: limit the number of addresses or POIs to return
        :param limit_stations: limit the number of stations to return
        :param location_types: limit the location types to return, available types are STATION,POI,ADDRESS
        :return: a list of locations
        """
        response = self._send_request(
            MVGRequests.location(
                query, limit_address_poi, limit_stations, location_types, self.headers
            )
        )
        return location.Locations(response)

    def get_messages(self, message_type=Optional[str]) -> messages.Messages:
        """
        Get the messages from the message board. Somehow similar to the ems ticker but it has more and different
         information.
        :param message_type: the type of the message, available types are INCIDENT,SCHEDULE_CHANGE
        :return: a list of messages
        """
        response = self._send_request(MVGRequests.messages(self.headers, message_type))
        return messages.Messages(response)

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
        """
        Get the connections between two stations or coordinates.
        You can use either station_id to station_id or coordinates to coordinates or station_id to coordinates.
        :param origin_station_id: the station id of the origin station
        :param destination_station_id: the station id of the destination station
        :param routing_date_time: the date and time of the departure or arrival for example 2023-06-25T20:04:47.552Z
        :param routing_date_time_is_arrival: if the routing_date_time is the arrival time or the departure time
        :param transport_types: the transport types to use, available types are SCHIFF,RUFTAXI,BAHN,UBAHN,TRAM,SBAHN,BUS
        ,REGIONAL_BUS
        :param origin_latitude: the latitude of the origin station
        :param origin_longitude: the longitude of the origin station
        :param destination_latitude: the latitude of the destination station
        :param destination_longitude: the longitude of the destination station
        :return: a list of connections
        """
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
        return connection.Connections(response)

    def get_lineinfo(self, language: Optional[str]) -> lineinfo.Infos:
        """
        Get the line info for some wired special lines like "lufthanse express bus"
        :param language: here the language argument also makes no difference in the response output.
        :return: a list of line info
        """
        response = self._send_request(MVGRequests.lineinfo(self.headers, language))
        return lineinfo.Infos(response)

    def get_stations(
        self, hash_: Optional[str] = None, world: Optional[bool] = None
    ) -> stations.Locations:
        """
        Get all the stations, like get_station_ids but with the hole station information.
        :param hash_: I don't know for what this hash is. (In the response is a hash, but if you send it again you get
        no response, so keep it empty)
        :param world: you can set the world to true or false. Maybe some day the MVG is operating worldwide.
        :return: a list of stations
        """
        response = self._send_request(MVGRequests.stations(self.headers, hash_, world))
        return stations.Locations(**response)

    def get_lines(self) -> line.Lines:
        """
        Get all the lines
        :return: a list of lines
        """
        response = self._send_request(MVGRequests.lines(self.headers))
        return line.Lines(response)

    def get_zoom_station(self, div_id: int) -> zoom_station.ZoomStation:
        """
        Get information about the availability TransportDevices at a station. Like elevators, escalators, etc.
        The information if similar to the information you get from the get_escalators_and_elevators
        :param div_id: an internal number that is associated with a station
        :return: a ZoomStation object
        """
        response = self._send_request(MVGRequests.zoom_station(div_id, self.headers))
        return zoom_station.ZoomStation(**response)

    def get_plan(self, div_id: int) -> bytes:
        """
        Get the plan of a station. The response is a pdf file in bytes.
        :param div_id: an internal number that is associated with a station
        :return: bytes of the pdf file
        """
        response = self._send_request(MVGRequests.plan(div_id, self.headers))
        return bytes(response)

    def get_zoom_station_out_of_order(
        self, div_id: int
    ) -> out_of_order.StationOutOfOrder:
        """
        Get the information about the availability of TransportDevices at a station. Like elevators, escalators, etc.
        :param div_id: an internal number that is associated with a station
        :return: a StationOutOfOrder object
        """
        response = self._send_request(
            MVGRequests.zoom_station_out_of_order(div_id, self.headers)
        )
        return out_of_order.StationOutOfOrder(**response)

    def get_vehicles_in_bounding_box(
        self, bbswlat: float, bbswlng: float, bbnelat: float, bbnelng: float
    ) -> vehicel.VehiclesAndSharingStations:
        """
        Get the vehicles and sharing stations in a bounding box. The bounding box is defined by two coordinates.
        :param bbswlat: Bounding box south-west latitude
        :param bbswlng: Bounding box south-west longitude
        :param bbnelat: Bounding box north-east latitude
        :param bbnelng: Bounding box north-east longitude
        :return: a VehiclesAndSharingStations object
        """
        response = self._send_request(
            MVGRequests.vehicle(bbswlat, bbswlng, bbnelat, bbnelng, self.headers)
        )
        return vehicel.VehiclesAndSharingStations(**response)

    def get_surrounding_plan(
        self, plan_id: str, world: bool = True, include_image_data: bool = True
    ) -> surounding_plans.Plan:
        """
        Get the surrounding plan of a station. If you include the image data you get a base64 encoded pdf of the plan.
        So you have to decode it first.
        :param plan_id: the first 2 letters of the station name in uppercase. For example "KA" for Karlsplatz
        :param world: again a world argument, but it makes no difference in the response output.
        :param include_image_data: a boolean if the response should include the image data of the plan
        :return:
        """
        response = self._send_request(
            MVGRequests.surrounding_plan(
                plan_id, self.headers, world, include_image_data
            )
        )
        return surounding_plans.Plan(**response)

    def get_surrounding_plans(
        self, world: Optional[bool] = True
    ) -> surounding_plans.Plans:
        """
        Get all the surrounding plans of all stations.
        :param world: again a world argument, but it makes no difference in the response output.
        :return: a list of surrounding plans
        """
        response = self._send_request(
            MVGRequests.surrounding_plans(self.headers, world)
        )
        return surounding_plans.Plans(response)


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
        except json.JSONDecodeError:
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

    async def get_departures(
        self,
        station_id: str,
        *,
        limit: Optional[int] = None,
        offset_minutes: Optional[int] = None,
        transport_types: Optional[Any] = None,
        language: Optional[str] = None,
    ) -> departure.Departures:
        """
        Get the departures for a station
        :param station_id: the same id as in get_station, for example de:09162:6 for Hauptbahnhof, and it can be
         obtained
        from a location method wenn the found Location is of the type STATION or from the get_all_stations method
        :param limit: the maximum number of departures to return
        :param offset_minutes: the offset in minutes from now for the departures
        :param transport_types: select specific transport types, available types are UBAHN,TRAM,BUS,SBAHN,SCHIFF
        :param language: the language ? I have no idea why this is here maybe for the language in the response. But I
        didn't see any difference when I changed it
        :return: a list of departures
        """
        response = await self._send_request(
            MVGRequests.departures(
                station_id,
                self.headers,
                limit=limit,
                offset_minutes=offset_minutes,
                transport_types=transport_types,
                language=language,
            )
        )
        return departure.Departures(response)

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

    async def get_location(
        self,
        query: str,
        limit_address_poi: Optional[int] = None,
        limit_stations: Optional[int] = None,
        location_types: Optional[List[str]] = None,
    ) -> location.Locations:
        """
        Get the location of a query, it can be a station name or a street name or a POI
        :param query: the Address or the station name or the POI name
        :param limit_address_poi: limit the number of addresses or POIs to return
        :param limit_stations: limit the number of stations to return
        :param location_types: limit the location types to return, available types are STATION,POI,ADDRESS
        :return: a list of locations
        """
        response = await self._send_request(
            MVGRequests.location(
                query, limit_address_poi, limit_stations, location_types, self.headers
            )
        )
        return location.Locations(response)

    async def get_messages(self, message_type=Optional[str]) -> messages.Messages:
        """
        Get the messages from the message board. Somehow similar to the ems ticker but it has more and different
         information.
        :param message_type: the type of the message, available types are INCIDENT,SCHEDULE_CHANGE
        :return: a list of messages
        """
        response = await self._send_request(
            MVGRequests.messages(self.headers, message_type)
        )
        return messages.Messages(response)

    async def get_connection(
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
        """
        Get the connections between two stations or coordinates.
        You can use either station_id to station_id or coordinates to coordinates or station_id to coordinates.
        :param origin_station_id: the station id of the origin station
        :param destination_station_id: the station id of the destination station
        :param routing_date_time: the date and time of the departure or arrival for example 2023-06-25T20:04:47.552Z
        :param routing_date_time_is_arrival: if the routing_date_time is the arrival time or the departure time
        :param transport_types: the transport types to use, available types are SCHIFF,RUFTAXI,BAHN,UBAHN,TRAM,SBAHN,BUS
        ,REGIONAL_BUS
        :param origin_latitude: the latitude of the origin station
        :param origin_longitude: the longitude of the origin station
        :param destination_latitude: the latitude of the destination station
        :param destination_longitude: the longitude of the destination station
        :return: a list of connections
        """
        response = await self._send_request(
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
        return connection.Connections(response)

    async def get_lineinfo(self, language: Optional[str]) -> lineinfo.Infos:
        """
        Get the line info for some wired special lines like "lufthanse express bus"
        :param language: here the language argument also makes no difference in the response output.
        :return: a list of line info
        """
        response = await self._send_request(
            MVGRequests.lineinfo(self.headers, language)
        )
        return lineinfo.Infos(response)

    async def get_stations(
        self, hash_: Optional[str] = None, world: Optional[bool] = None
    ) -> stations.Locations:
        """
        Get all the stations, like get_station_ids but with the hole station information.
        :param hash_: I don't know for what this hash is. (In the response is a hash, but if you send it again you get
        no response, so keep it empty)
        :param world: you can set the world to true or false. Maybe some day the MVG is operating worldwide.
        :return: a list of stations
        """
        response = await self._send_request(
            MVGRequests.stations(self.headers, hash_, world)
        )
        return stations.Locations(**response)

    async def get_lines(self) -> line.Lines:
        """
        Get all the lines
        :return: a list of lines
        """
        response = await self._send_request(MVGRequests.lines(self.headers))
        return line.Lines(response)

    async def get_zoom_station(self, div_id: int) -> zoom_station.ZoomStation:
        """
        Get information about the availability TransportDevices at a station. Like elevators, escalators, etc.
        The information if similar to the information you get from the get_escalators_and_elevators
        :param div_id: an internal number that is associated with a station
        :return: a ZoomStation object
        """
        response = await self._send_request(
            MVGRequests.zoom_station(div_id, self.headers)
        )
        return zoom_station.ZoomStation(**response)

    async def get_plan(self, div_id: int) -> bytes:
        """
        Get the plan of a station. The response is a pdf file in bytes.
        :param div_id: an internal number that is associated with a station
        :return: bytes of the pdf file
        """
        response = await self._send_request(MVGRequests.plan(div_id, self.headers))
        return bytes(response)

    async def get_zoom_station_out_of_order(
        self, div_id: int
    ) -> out_of_order.StationOutOfOrder:
        """
        Get the information about the availability of TransportDevices at a station. Like elevators, escalators, etc.
        :param div_id: an internal number that is associated with a station
        :return: a StationOutOfOrder object
        """
        response = await self._send_request(
            MVGRequests.zoom_station_out_of_order(div_id, self.headers)
        )
        return out_of_order.StationOutOfOrder(**response)

    async def get_vehicles_in_bounding_box(
        self, bbswlat: float, bbswlng: float, bbnelat: float, bbnelng: float
    ) -> vehicel.VehiclesAndSharingStations:
        """
        Get the vehicles and sharing stations in a bounding box. The bounding box is defined by two coordinates.
        :param bbswlat: Bounding box south-west latitude
        :param bbswlng: Bounding box south-west longitude
        :param bbnelat: Bounding box north-east latitude
        :param bbnelng: Bounding box north-east longitude
        :return: a VehiclesAndSharingStations object
        """
        response = await self._send_request(
            MVGRequests.vehicle(bbswlat, bbswlng, bbnelat, bbnelng, self.headers)
        )
        return vehicel.VehiclesAndSharingStations(**response)

    async def get_surrounding_plan(
        self, plan_id: str, world: bool = True, include_image_data: bool = True
    ) -> surounding_plans.Plan:
        """
        Get the surrounding plan of a station. If you include the image data you get a base64 encoded pdf of the plan.
        So you have to decode it first.
        :param plan_id: the first 2 letters of the station name in uppercase. For example "KA" for Karlsplatz
        :param world: again a world argument, but it makes no difference in the response output.
        :param include_image_data: a boolean if the response should include the image data of the plan
        :return:
        """
        response = await self._send_request(
            MVGRequests.surrounding_plan(
                plan_id, self.headers, world, include_image_data
            )
        )
        return surounding_plans.Plan(**response)

    async def get_surrounding_plans(
        self, world: Optional[bool] = True
    ) -> surounding_plans.Plans:
        """
        Get all the surrounding plans of all stations.
        :param world: again a world argument, but it makes no difference in the response output.
        :return: a list of surrounding plans
        """
        response = await self._send_request(
            MVGRequests.surrounding_plans(self.headers, world)
        )
        return surounding_plans.Plans(response)
