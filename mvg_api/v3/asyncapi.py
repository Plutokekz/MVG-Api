# Please note: the sync and async api variants are identical except for async/await keywords.
# To reduce manual editing the both apis, only edit the async variant.
# Then use the following command to quickly generate the sync variant from the async variant.
#
# [ -f asyncapi.py ] && echo "# DO NOT EDIT - DERIVED FROM asyncapi.py" > syncapi.py && sed -e 's/async def/def/g' -e 's/= await/=/g' -e 's/AsyncApi/SyncApi/g' -e 's/AsyncClient/Client/g' asyncapi.py >> syncapi.py


import json
from typing import Dict, Any, Optional, List
from pathlib import Path
import httpx
import datetime

from mvg_api.v3.schemas import (
    aushang,
    connection,
    departure,
    line,
    location,
    messages,
    station,
    stations,
    ticker,
    zoom,
)
from mvg_api.v3.requests import MVGRequests, RequestFailed


class AsyncApi:
    __slots__ = ("client", "do_log_responses", "headers")

    client: httpx.AsyncClient
    do_log_responses: bool
    headers: Dict[str, str]

    def __init__(self, client: httpx.Client = None, do_log_responses: bool = False):
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
            json.dump(response.json(), f, indent=2)

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
        response = await self._send_request(MVGRequests.aushang(self.headers, mvg_id))
        return aushang.Aushaenge(response)

    async def get_connections(
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
        :param transport_types: limit departures to specific transport types
        :param origin_latitude: the latitude of the origin station
        :param origin_longitude: the longitude of the origin station
        :param destination_latitude: the latitude of the destination station
        :param destination_longitude: the longitude of the destination station
        :return: a list of connections
        """
        response = await self._send_request(
            MVGRequests.connections(
                self.headers,
                origin_station_id,
                destination_station_id,
                routing_date_time,
                routing_date_time_is_arrival=routing_date_time_is_arrival,
                transport_types=transport_types,
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
        :param station_id: global id of the station
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
        location_types: Optional[List[str]] = None,
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

    async def get_station_ids(self) -> List[str]:
        """
        Get all the station ids
        :return: returns a list of strings with all the station ids that are available
        """
        response = await self._send_request(MVGRequests.station_ids(self.headers))
        return list(response)

    async def get_station(self, station_id: str) -> station.Station:
        """
        Get a station by its id the Station id can be found in the get_all_stations list, or it can be obtained from a
        location method wenn the found Location is of the type STATION
        :param station_id: for example de:09162:6 for Hauptbahnhof
        :return: a Station
        """
        response = await self._send_request(MVGRequests.station(self.headers, station_id))
        return station.Station(**response)

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

    async def get_ticker(self) -> ticker.Messages:
        """
        Get ticker messages, updates about the disruptions and planed works on the MVG train network
        There 2 types of messages DISRUPTION and PLANNED
        :return: a list es messages
        """
        response = await self._send_request(MVGRequests.ticker(self.headers))
        return ticker.Messages(response)

    async def get_zoom(self, efa_id: int) -> zoom.ZoomStation:
        """
        Get the escalators and elevators location and status for a station
        :param efa_id: an integer number that is associated with a station. It is included in the Station object but
        under the name of divId for some reason.
        :return: a ZoomStation object
        """
        response = await self._send_request(
            MVGRequests.zoom(self.headers, efa_id)
        )
        return zoom.ZoomStation(**response)

    async def find_location(self, query: str) -> location.Location:
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

    async def find_location_station(self, query: str) -> location.Location:
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
