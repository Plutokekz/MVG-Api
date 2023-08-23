import datetime
from typing import List, Optional

from Levenshtein import ratio

from mvg_api.v1.mvg import LocationNotFound
from mvg_api.v2.api import SyncApi, AsyncApi
from mvg_api.v2.schemas.connection import Connections
from mvg_api.v2.schemas.departure import Departures
from mvg_api.v2.schemas.location import LocationType, Location


class SyncMVG(SyncApi):
    def __init__(self):
        super().__init__()

    def _match_location(
        self, location_str: str, location_types: Optional[List[LocationType]] = None
    ) -> Location:
        locations = self.get_location(location_str, location_types=location_types)
        for location in locations:
            if location.type == LocationType.STATION:
                if ratio(location_str, location.name) > 0.8:
                    return location
            if location.type == LocationType.ADDRESS:
                if ratio(location_str, location.street) > 0.75:
                    return location
        raise LocationNotFound(f"no location found for {location_str}")

    def get_departures_by_name(self, name: str, **kwargs) -> Departures:
        """
        Get the departures for a given station name, the keyword arguments are the same as in get_departures
        :param name: of the station
        :return: a list of departures
        """
        location = self._match_location(name, location_types=[LocationType.STATION])
        return self.get_departures(location.globalId, **kwargs)

    def _location_to_connection_args(
        self, start_location: Location, stop_location: Location
    ):
        args = {}
        if start_location.type == LocationType.STATION:
            args["origin_station_id"] = start_location.globalId
        if stop_location.type == LocationType.STATION:
            args["destination_station_id"] = stop_location.globalId
        if start_location.type == LocationType.ADDRESS:
            args["origin_latitude"] = start_location.latitude
            args["origin_longitude"] = start_location.longitude
        if stop_location.type == LocationType.ADDRESS:
            args["destination_latitude"] = stop_location.latitude
            args["destination_longitude"] = stop_location.longitude
        return args

    def get_connection_by_name(
        self,
        start: str,
        stop: str,
        start_datetime: Optional[datetime.datetime] = None,
        date_time_is_arrival: bool = False,
        **kwargs,
    ) -> Connections:
        """
        Get a connection between two locations by the station or address name, the keyword arguments are the same as in
        get_connection
        :param start: the start location/ address name
        :param stop: the destination location/ address name
        :param start_datetime:  the start time of the connection in the following format: %Y-%m-%dT%H:%M:%S.%fZ
        :param date_time_is_arrival: if the start time is the arrival time
        :param kwargs: the keyword arguments for the get_connection method, they will overwrite the default values
        :return: a list of connections
        """
        start_location = self._match_location(
            start, location_types=[LocationType.STATION, LocationType.ADDRESS]
        )
        stop_location = self._match_location(
            stop, location_types=[LocationType.STATION, LocationType.ADDRESS]
        )

        args = self._location_to_connection_args(start_location, stop_location)

        if start_datetime is None:
            start_datetime = datetime.datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )

        args["routing_date_time"] = start_datetime
        args["routing_date_time_is_arrival"] = date_time_is_arrival

        args.update(kwargs)

        return self.get_connection(**args)  # pylint: disable=missing-kwoa


class AsyncMVG(AsyncApi):
    def __init__(self):
        super().__init__()

    async def _match_location(
        self, location_str: str, location_types: Optional[List[LocationType]] = None
    ) -> Location:
        locations = await self.get_location(location_str, location_types=location_types)
        for location in locations:
            if location.type == LocationType.STATION:
                if ratio(location_str, location.name) > 0.8:
                    return location
            if location.type == LocationType.ADDRESS:
                if ratio(location_str, location.street) > 0.75:
                    return location
        raise LocationNotFound(f"no location found for {location_str}")

    async def get_departures_by_name(self, name: str, **kwargs) -> Departures:
        """
        Get the departures for a given station name, the keyword arguments are the same as in get_departures
        :param name: of the station
        :return: a list of departures
        """
        location = await self._match_location(
            name, location_types=[LocationType.STATION]
        )
        return await self.get_departures(location.globalId, **kwargs)

    def _location_to_connection_args(
        self, start_location: Location, stop_location: Location
    ):
        args = {}
        if start_location.type == LocationType.STATION:
            args["origin_station_id"] = start_location.globalId
        if stop_location.type == LocationType.STATION:
            args["destination_station_id"] = stop_location.globalId
        if start_location.type == LocationType.ADDRESS:
            args["origin_latitude"] = start_location.latitude
            args["origin_longitude"] = start_location.longitude
        if stop_location.type == LocationType.ADDRESS:
            args["destination_latitude"] = stop_location.latitude
            args["destination_longitude"] = stop_location.longitude
        return args

    async def get_connection_by_name(
        self,
        start: str,
        stop: str,
        start_datetime: Optional[datetime.datetime] = None,
        date_time_is_arrival: bool = False,
        **kwargs,
    ) -> Connections:
        """
        Get a connection between two locations by the station or address name, the keyword arguments are the same as in
        get_connection
        :param start: the start location/ address name
        :param stop: the destination location/ address name
        :param start_datetime:  the start time of the connection in the following format: %Y-%m-%dT%H:%M:%S.%fZ
        :param date_time_is_arrival: if the start time is the arrival time
        :param kwargs: the keyword arguments for the get_connection method, they will overwrite the default values
        :return: a list of connections
        """
        start_location = await self._match_location(
            start, location_types=[LocationType.STATION, LocationType.ADDRESS]
        )
        stop_location = await self._match_location(
            stop, location_types=[LocationType.STATION, LocationType.ADDRESS]
        )

        args = self._location_to_connection_args(start_location, stop_location)

        if start_datetime is None:
            start_datetime = datetime.datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )

        args["routing_date_time"] = start_datetime
        args["routing_date_time_is_arrival"] = date_time_is_arrival

        args.update(kwargs)

        return await self.get_connection(**args)  # pylint: disable=missing-kwoa


if __name__ == "__main__":
    sync_mvg = SyncMVG()
    print(sync_mvg.get_departures_by_name("Marienplatz"))
    print(sync_mvg.get_connection_by_name("Marienplatz", "Hauptbahnhof"))
    import asyncio

    async_mvg = AsyncMVG()
    print(asyncio.run(async_mvg.get_departures_by_name("Marienplatz")))
    async_mvg = AsyncMVG()
    print(asyncio.run(async_mvg.get_connection_by_name("Marienplatz", "Hauptbahnhof")))
