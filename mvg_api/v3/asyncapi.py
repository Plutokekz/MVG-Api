# Please note: the sync and async api variants are identical except for async/await keywords.
# To reduce manual editing the both apis, only edit the async variant.
# Then run scripts/generate_syncapi.sh to regenerate the sync variant.


import json
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import datetime
import logging

import httpx

from mvg_api.v3.schemas import (
    aushang,
    connection,
    departure,
    line,
    location,
    messages,
    nearby,
    station,
    stations,
    ticker,
    ubahn_map,
    zoom,
)
from mvg_api.v3.requests import MVGRequests, RequestFailed


logger = logging.getLogger("mvg-api")
logger.setLevel(logging.DEBUG)


class AsyncApi:
    __slots__ = ("client", "do_log_responses", "headers")

    client: httpx.AsyncClient
    do_log_responses: bool
    headers: Dict[str, str]

    def __init__(self, client: Optional[httpx.AsyncClient] = None, do_log_responses: bool = False):
        """
        Creates a new API instance to send requests the MVG backend.
        This instance can be used to send multiple requests, thereby reusing the http client.

        :param client: a specific client instance, otherwise a new client is created.
        :param do_log_responses: whether the responses of the MVG api should be logged for debugging purposes.
        """
        self.client = client if client is not None else httpx.AsyncClient()
        self.do_log_responses = do_log_responses
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "sec-gpc": "1",
        }

    def _log_response(self, request: httpx.Request, response: httpx.Response):
        """
        Logs the response of an MVG api request to a file in the dir `responselog` for inspection and debugging
        """
        if not (Path.cwd() / "responselog").exists():
            (Path.cwd() / "responselog").mkdir()
        output = "responselog/response-"
        output += datetime.datetime.now().strftime("%Y%m%d-T%H%M%S") + "-"
        url = str(request.url).replace("/", "-").replace(":", "-")
        if len(url) > 80:
            url = url[:80]
        output += url + ".json"

        with open(output, "w", encoding="utf-8") as f:
            try:
                json.dump(response.json(), f, indent=2)
            except (json.JSONDecodeError, ValueError):
                f.write(response.text)

    async def _send_request(self, request: httpx.Request) -> Any:
        response = await self.client.send(request)
        if self.do_log_responses:
            self._log_response(request, response)

        if response.status_code != 200:
            self._log_response(request, response)
            raise RequestFailed(
                f"Request failed with status code: {response.status_code} and response {response.text}"
            )
        try:
            return response.json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            return response.content

    async def get_aushang(self, mvg_id: str) -> aushang.Aushaenge:
        """
        Get the aushang of a station, like timetables or maps that may be located at an information display case at a station.
        :param mvg_id: the MVG id of the station.
        :return: a list of aushaenge
        """
        if mvg_id == "":  # 400 Bad Request - mvg_id must not be empty
            return aushang.Aushaenge([])
        response = await self._send_request(MVGRequests.aushang(self.headers, mvg_id))
        return aushang.Aushaenge(response)

    async def get_connections(  # pylint: disable=too-many-arguments
        self,
        origin_station_id: str,
        destination_station_id: str,
        routing_date_time: str,
        *,
        routing_date_time_is_arrival: bool = False,
        transport_types: Optional[str] = "SCHIFF,UBAHN,TRAM,SBAHN,BUS,REGIONAL_BUS,BAHN",
        route_type: Optional[str] = "LEAST_TIME",
        change_speed: Optional[str] = "NORMAL",
        accessibility_options: Optional[str] = None,
        via_station_id: Optional[str] = None,
        via_dwell_time_minutes: Optional[int] = None,
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
        :param transport_types: limit to specific transport types; possible are: SCHIFF,UBAHN,TRAM,SBAHN,BUS,REGIONAL_BUS,BAHN,RUFTAXI
        :param route_type: LEAST_TIME (Schnelle Route), LEAST_INTERCHANGES (Wenige Umstiege), LEAST_WALKING (Wenig Fußweg)
        :param change_speed: SLOW (Langsam), NORMAL (Normal), FAST (Schnell)
        :param accessibility_options: NO_SOLID_STAIRS (keine Treppen), NO_ESCALATORS (keine Rolltreppen), NO_ELEVATORS (keine Aufzüge)
        :param via_station_id: global id of a via station that should be part of the route
        :param via_dwell_time_minutes: time at the via station between arrival and departure.
            Omission or value 0 will cause the via station to be ignored.
        :param origin_latitude: the latitude of the origin station
        :param origin_longitude: the longitude of the origin station
        :param destination_latitude: the latitude of the destination station
        :param destination_longitude: the longitude of the destination station
        :return: a list of connections
        """
        if via_station_id and (not via_dwell_time_minutes or int(via_dwell_time_minutes) <= 0):
            logger.warning("Via dwelltime must be > 0 when via station is specified; ignoring via station.")
            via_station_id = None
            via_dwell_time_minutes = None
        response = await self._send_request(
            MVGRequests.connections(
                self.headers,
                origin_station_id,
                destination_station_id,
                routing_date_time,
                routing_date_time_is_arrival=routing_date_time_is_arrival,
                transport_types=transport_types,
                route_type=route_type,
                change_speed=change_speed,
                accessibility_options=accessibility_options,
                via_station_id=via_station_id,
                via_dwell_time_minutes=via_dwell_time_minutes,
                origin_latitude=origin_latitude,
                origin_longitude=origin_longitude,
                destination_latitude=destination_latitude,
                destination_longitude=destination_longitude,
            )
        )
        return connection.Connections(response)

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
        :param station_id: IFOPT global id of the station
        :param limit: the maximum number of departures to return
        :param offset_minutes: an offset in minutes from now
        :param transport_types: limit departures to specific transport types
        :return: a list of departures
        """
        response = await self._send_request(
            MVGRequests.departures(
                self.headers,
                station_id,
                limit=limit,
                offset_minutes=offset_minutes,
                transport_types=transport_types,
                language=language,
            )
        )
        return departure.Departures(response)

    async def get_lines(self, station_id: Optional[str] = None) -> line.Lines:
        """
        Get all lines in the MVV area or limited to a specific station
        :param station_id: global id of a station or none to get all lines
        :return: a list of lines
        """
        response = await self._send_request(MVGRequests.lines(self.headers, station_id=station_id))
        return line.Lines(response)

    async def get_locations(
        self,
        query: str,
        limit_address_poi: Optional[int] = None,
        limit_stations: Optional[int] = None,
        location_types: Optional[List[location.LocationType]] = None,
    ) -> location.Locations:
        """
        Get all locations for a text query
        :param query: a text query, that may be a partical address, station name or POI name
        :param limit_address_poi: limit the number of addresses or POIs to return
        :param limit_stations: limit the number of stations to return
        :param location_types: limit the location types to return; available types are STATION,POI,ADDRESS
        :return: a list of locations
        """
        if query == "":  # 400 Bad Request - query must not be empty
            return location.Locations([])
        response = await self._send_request(
            MVGRequests.locations(self.headers, query, limit_address_poi, limit_stations, location_types)
        )
        return location.Locations(response)

    async def get_messages(self, message_type: Optional[str] = None) -> messages.Messages:
        """
        Get all messages about incidents or schedule changes.
        :param message_type: filters messages by type; available types are INCIDENT,SCHEDULE_CHANGE
        :return: a list of messages
        """
        response = await self._send_request(MVGRequests.messages(self.headers, message_type))
        return messages.Messages(response)

    async def get_nearby(self, latitude: Optional[float], longitude: Optional[float]) -> nearby.Stations:
        """
        Get a list of nearby stations with the respective linear distance.
        :return: a list of stations
        """
        if latitude is None or longitude is None:  # 400 Bad Request - lat/lon must not be empty
            return nearby.Stations([])
        response = await self._send_request(MVGRequests.nearby(self.headers, latitude, longitude))
        return nearby.Stations(response)

    async def get_station_ids(self) -> List[str]:
        """
        Get all IFOPT global ids of stations in the MVG area; primarily munich.
        Does not yield station ids in the MVV (except MVG).
        :return: returns a list of global id strings
        """
        response = await self._send_request(MVGRequests.station_ids(self.headers))
        return list(response)

    async def get_station(self, station_id: str) -> Optional[station.Station]:
        """
        Get details about a station by its IFOPT global id.
        :param station_id: IFOPT global id of a station
        :return: a single station or None
        """
        if station_id == "":  # identical to get_stations endpoint if empty
            return None
        response = await self._send_request(MVGRequests.station(self.headers, station_id))
        return station.Station(**response)

    async def get_stations(
        self, hash_: Optional[str] = None, world: Optional[bool] = None
    ) -> stations.Stations:
        """
        Get all stations in the MVV. This is more extensive than get_station_ids.
        This is a huge result of ~13MiB with a total of 44130 stations (as of 2026-02-15).

        :param hash_: A hash, presumably identifying whether there was a change in the station
            data between two requests, such that no new data has to be sent. When the hash,
            obtained from the result of a previous request is submitted, the result is empty
            (perhaps except if there is new data).
        :param world: unknown, does not change the result, except for a different hash.
        :return: a list of MVV stations.
        """
        response = await self._send_request(
            MVGRequests.stations(self.headers, hash_, world)
        )
        return stations.Stations(**response)

    async def get_ticker(self) -> ticker.Messages:
        """
        Get ticker messages. This is somewhat identical to the result of get_messages but is
        apparently limited to services of MVG only (i.e. UBAHN, TRAM, BUS <200)
        :return: a list of messages
        """
        response = await self._send_request(MVGRequests.ticker(self.headers))
        return ticker.Messages(response)

    async def get_ubahn_map(self, uuid: str = "a5ac8f68-1f4a-45c0-acc2-7cbdb3740f58") -> ubahn_map.UbahnMap:
        """
        Get pixel coordinate information about all ubahn stations to display on the network map.
        Practical use in conjunction with get_zoom for all stations
        :param uuid: permanent value in the path of the request url; usage unknown; might change.
        :return: an UbahnMap object
        """
        response = await self._send_request(MVGRequests.ubahn_map(self.headers, uuid))
        return ubahn_map.UbahnMap(ubahn_map.simplify_api_response(response))

    async def get_zoom(self, efa_id: Optional[str] = None) -> Union[zoom.ZoomStation, zoom.ZoomStations]:
        """
        Get zoom information that contains the status, names and positions of escalators and elevators in an MVG (typically ubahn) station.
        If no efa id is specified, the status of all stations is returned.
        :param efa_id: divaId/efaId of the station or none.
        :return: a ZoomStation object if an efa id is given or a ZoomStations object if data of all stations is requested.
        """
        response = await self._send_request(MVGRequests.zoom(self.headers, efa_id))
        if isinstance(response, list):
            return zoom.ZoomStations(response)
        return zoom.ZoomStation(**response)

    async def find_location(self, query: str) -> Optional[location.Location]:
        """
        Search a location.
        Selects the first matching one from the list of locations returned by get_locations.

        :param query: a query string with a station name, address, etc
        :return: the first matching location or None
        """

        matching_locations = await self.get_locations(query)
        if matching_locations:
            return matching_locations[0]
        return None

    async def find_location_station(self, query: str) -> Optional[location.Location]:
        """
        Search a location of type station.
        Selects the first matching one from the list of locations returned by get_locations.

        :param query: a query string with a station name, address, etc
        :return: the first matching location or None
        """

        matching_locations = await self.get_locations(query)
        matching_stations = [l for l in matching_locations if l.type == location.LocationType.STATION]
        if matching_stations:
            return matching_stations[0]
        return None
