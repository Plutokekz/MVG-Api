# DO NOT EDIT - DERIVED FROM asyncapi.py
# sync and async api are identical except for async/await keywords
# use the following command to quickly generate the sync variant from the async variant when functions were changed
#
# echo "# DO NOT EDIT - DERIVED FROM asyncapi.py" > syncapi.py && sed -e 's/def/def/g' -e 's/=/=/g' -e 's/SyncApi/SyncApi/g' -e 's/Client/Client/g' asyncapi.py >> syncapi.py


import json
from typing import Dict, Any, Optional, List
from .requests import MVGRequests, RequestFailed

import httpx

from mvg_api.v3.schemas import (
    aushang,
    connection,
    departure,
    line,
    location,
    ems,
    station,
    transportdevice,
)
from mvg_api.v3.schemas.location import LocationType


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

    def get_aushang(self, plan_id: str) -> aushang.Aushaenge:
        """
        Get the aushang for a station, get all Playn that a currently active in a stations blackboard.
        :param plan_id: I am not sure bit it seems to be the first 2 letters of the station name in uppercase.
         For example
        KA for Karlsplatz
        :return: a list of aushaenge
        """
        response = self._send_request(MVGRequests.aushang(self.headers, plan_id))
        return aushang.Aushaenge(response)

    def get_connections(
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

    def get_connections_by_name(
        self,
        origin_station_name: str,
        destination_station_name: str,
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
        :param origin_station_name: the station name of the origin station
        :param destination_station_name: the station name of the destination station
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
        origin_stations = self.get_locations(origin_station_name)
        origin_station_id = origin_stations[0].globalId if origin_stations else None
        destination_stations = self.get_locations(destination_station_name)
        destination_station_id = destination_stations[0].globalId if destination_stations else None
        if origin_station_id is None or destination_station_id is None:
            raise RequestFailed(
                f"Unable to look up origin and/or destination; origin_station_name={origin_station_name} destination_station_name={destination_station_name}")
        response = self._send_request(
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
                self.headers,
                station_id,
                limit=limit,
                offset_minutes=offset_minutes,
                transport_types=transport_types,
                language=language,
            )
        )
        return departure.Departures(response)

    def get_departures_by_name(
        self,
        station_name: str,
        *,
        limit: Optional[int] = None,
        offset_minutes: Optional[int] = None,
        transport_types: Optional[Any] = None,
        language: Optional[str] = None,
    ) -> departure.Departures:
        """
        Get the departures for a station
        :param station_name: the name of a station to lookup departures of
        :param limit: the maximum number of departures to return
        :param offset_minutes: the offset in minutes from now for the departures
        :param transport_types: select specific transport types, available types are UBAHN,TRAM,BUS,SBAHN,SCHIFF
        :param language: the language ? I have no idea why this is here maybe for the language in the response. But I
        didn't see any difference when I changed it
        :return: a list of departures
        """
        stations = self.get_locations(station_name)
        station_id = stations[0].globalId if stations else None
        if station_id is None:
            raise RequestFailed(f"Unable to look up station; station_name={station_name}")
        response = self._send_request(
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

    def get_lines(self, station_id: Optional[str] = None) -> line.Lines:
        """
        Get all the lines
        :return: a list of lines
        """
        response = self._send_request(MVGRequests.lines(self.headers, station_id=station_id))
        return line.Lines(response)

    def get_locations(
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
        if query == "":  # 400 Bad Request - query must not be empty
            return location.Locations([])
        response = self._send_request(
            MVGRequests.locations(self.headers, query, limit_address_poi, limit_stations, location_types)
        )
        return location.Locations(response)


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
        response = self._send_request(
            MVGRequests.station(station_id, self.headers)
        )
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

    def get_station_ids(self) -> List[str]:
        """
        Get all the station ids
        :return: returns a list of strings with all the station ids that are available
        """
        response = self._send_request(MVGRequests.station_ids(self.headers))
        return list(response)
