import datetime
from typing import List

from Levenshtein import ratio

from mvg_api.v1.api import Api, AsyncApi
from mvg_api.v1.schemas.route import Location, LocationType, Connections, LocationList
from mvg_api.v1.schemas.ticker import TickerList, SlimList


class LocationNotFound(Exception):
    """
    If there is no locations that matches the input String this exception is raised
    """


class MVG:
    api: Api

    def __init__(self):
        self.api = Api()

    def _match_location(self, location_str: str) -> Location:
        locations = self.api.get_location(location_str)
        for location in locations:
            if location.type == LocationType.STATION:
                if ratio(location_str, location.name) > 0.8:
                    return location
            if location.type == LocationType.ADDRESS:
                if ratio(location_str, location.street) > 0.75:
                    return location
        raise LocationNotFound(f"no location found for {location_str}")

    def get_rout(
        self,
        location_from,
        location_to,
        *,
        _time: datetime.datetime = None,
        arrival_time: bool = False,
        transport_types: str = "SCHIFF,RUFTAXI,BAHN,UBAHN,TRAM,SBAHN,BUS,REGIONAL_BUS",
    ) -> Connections:
        """
        Get a MVG rout, starting at the location_from and ending at location_to, if one of the given strings don't match
        any location a LocationNotFound Exception will be raised
        :param transport_types:
        :param arrival_time: make the _time the arrival time not the start time
        :param _time: datetime for the start of the rout
        :param location_from: your starting location
        :param location_to:  your destination
        :return: a list of possible connections
        """
        from_ = self._match_location(location_from)
        to_ = self._match_location(location_to)
        if from_.type == LocationType.STATION:
            location_from = from_.globalId
        if to_.type == LocationType.STATION:
            location_to = to_.globalId
        return self.api.get_route(
            origin_station_global_id=location_from,
            destination_station_global_id=location_to,
            routing_date_time=_time,
            transport_types=transport_types,
            routing_date_time_is_arrival=arrival_time,
        )

    def get_ticker(self) -> TickerList:
        """
        get a list of all disruptions
        :return:
        """
        return self.api.get_ticker()

    def get_slim(self) -> SlimList:
        """
        get a List of all unplanned disruption in the light edition
        :return:
        """
        return self.api.get_slim()

    def get_current_date(self) -> datetime.datetime:
        """
        Get the current datetime from MVG
        :return: datetime object
        """
        return self.api.get_current_date()

    def get_global_station_ids(self) -> List[str]:
        """
        A list of the Station ids (I think it's all the available ons)
        :return:
        """
        return self.api.get_station_global_ids()

    def get_location(self, name: str) -> LocationList:
        """
        Get al List of Location by the given name
        :param name:
        :return:
        """
        return self.api.get_location(name)


class AsyncMVG:
    api: AsyncApi

    def __init__(self):
        self.api = AsyncApi()

    async def _match_location(self, location_str: str) -> Location:
        locations = await self.api.get_location(location_str)
        for location in locations:
            if location.type == LocationType.STATION:
                if ratio(location_str, location.name) > 0.8:
                    return location
            if location.type == LocationType.ADDRESS:
                if ratio(location_str, location.street) > 0.75:
                    return location
        raise LocationNotFound(f"no location found for {location_str}")

    async def get_rout(
        self,
        location_from,
        location_to,
        *,
        _time: datetime.datetime = None,
        arrival_time: bool = False,
        transport_types: str = "SCHIFF,RUFTAXI,BAHN,UBAHN,TRAM,SBAHN,BUS,REGIONAL_BUS",
    ) -> Connections:
        """
        Get a MVG rout, starting at the location_from and ending at location_to, if one of the given strings don't match
        any location a LocationNotFound Exception will be raised
        :param transport_types:
        :param arrival_time: make the _time the arrival time not the start time
        :param _time: datetime for the start of the rout
        :param location_from: your starting location
        :param location_to:  your destination
        :return: a list of possible connections
        """
        from_ = await self._match_location(location_from)
        to_ = await self._match_location(location_to)
        if from_.type == LocationType.STATION:
            location_from = from_.globalId
        if to_.type == LocationType.STATION:
            location_to = to_.globalId
        return await self.api.get_route(
            origin_station_global_id=location_from,
            destination_station_global_id=location_to,
            routing_date_time=_time,
            transport_types=transport_types,
            routing_date_time_is_arrival=arrival_time,
        )

    async def get_ticker(self) -> TickerList:
        """
        get a list of all disruptions
        :return:
        """
        return await self.api.get_ticker()

    async def get_slim(self) -> SlimList:
        """
        get a List of all unplanned disruption in the light edition
        :return:
        """
        return await self.api.get_slim()

    async def get_current_date(self) -> datetime.datetime:
        """
        Get the current datetime from MVG
        :return: datetime object
        """
        return await self.api.get_current_date()

    async def get_global_station_ids(self) -> List[str]:
        """
        A list of the Station ids (I think it's all the available ons)
        :return:
        """
        return await self.api.get_station_global_ids()

    async def get_location(self, name: str) -> LocationList:
        """
        Get al List of Location by the given name
        :param name:
        :return:
        """
        return await self.api.get_location(name)


if __name__ == "__main__":
    mvg = MVG()
    for connection in mvg.get_rout("Holzkirchen", "Garching").connectionList:
        for connection_part in connection.parts:
            print(connection_part.exitLetter)
            print(f"{connection_part.from_.name}->{connection_part.to.name}")
        print(f"Entfernung {connection.distance}")
