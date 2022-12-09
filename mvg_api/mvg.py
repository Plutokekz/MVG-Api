import datetime
from typing import List

from Levenshtein import ratio

from mvg_api.api.api import Api, AsyncApi
from mvg_api.models.route import Location, LocationType, Connections, LocationList
from mvg_api.models.ticker import TickerList, SlimList


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
        for location in locations.locations:
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
    ) -> Connections:
        """
        Get a MVG rout, starting at the location_from and ending at location_to, if one of the given strings don't match
        any location a LocationNotFound Exception will be raised
        :param sbahn: use sbahn
        :param tram: use tram
        :param bus: use bus
        :param ubahn: use ubahn
        :param change_limit: max changes between start and end destination
        :param max_walk_time_to_dest: max walk time in minutes to start location
        :param max_walk_time_to_start: max walk time in minutes to end location
        :param arrival_time: make the _time the arrival time not the start time
        :param transport_type_call_taxi: use taxi
        :param _time: datetime for the start of the rout
        :param sap_tickets: show available tickets
        :param location_from: your starting location
        :param location_to:  your destination
        :return: a list of possible connections
        """
        from_ = self._match_location(location_from)
        to_ = self._match_location(location_to)
        if from_.type == LocationType.STATION:
            location_from = from_.id
        else:
            location_from = (from_.latitude, from_.longitude)
        if to_.type == LocationType.STATION:
            location_to = to_.id
        else:
            location_to = (to_.latitude, to_.longitude)
        return self.api.get_route(
            location_from,
            location_to,
            _time=_time,
            sap_tickets=sap_tickets,
            transport_type_call_taxi=transport_type_call_taxi,
            arrival_time=arrival_time,
            max_walk_time_to_start=max_walk_time_to_start,
            max_walk_time_to_dest=max_walk_time_to_dest,
            change_limit=change_limit,
            ubahn=ubahn,
            sbahn=sbahn,
            tram=tram,
            bus=bus,
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
        for location in locations.locations:
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
    ) -> Connections:
        """
        Get a MVG rout, starting at the location_from and ending at location_to, if one of the given strings don't match
        any location a LocationNotFound Exception will be raised
        :param sbahn: use sbahn
        :param tram: use tram
        :param bus: use bus
        :param ubahn: use ubahn
        :param change_limit: max changes between start and end destination
        :param max_walk_time_to_dest: max walk time in minutes to start location
        :param max_walk_time_to_start: max walk time in minutes to end location
        :param arrival_time: make the _time the arrival time not the start time
        :param transport_type_call_taxi: use taxi
        :param _time: datetime for the start of the rout
        :param sap_tickets: show available tickets
        :param location_from: your starting location
        :param location_to:  your destination
        :return: a list of possible connections
        """
        from_ = await self._match_location(location_from)
        to_ = await self._match_location(location_to)
        if from_.type == LocationType.STATION:
            location_from = from_.id
        else:
            location_from = (from_.latitude, from_.longitude)
        if to_.type == LocationType.STATION:
            location_to = to_.id
        else:
            location_to = (to_.latitude, to_.longitude)
        return await self.api.get_route(
            location_from,
            location_to,
            _time=_time,
            sap_tickets=sap_tickets,
            transport_type_call_taxi=transport_type_call_taxi,
            arrival_time=arrival_time,
            max_walk_time_to_start=max_walk_time_to_start,
            max_walk_time_to_dest=max_walk_time_to_dest,
            change_limit=change_limit,
            ubahn=ubahn,
            sbahn=sbahn,
            tram=tram,
            bus=bus,
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
        print(f"Von {connection.from_.name} nach {connection.to.name}")
        print(f"Abfahrt {connection.arrival - connection.departure}")
        for connection_part in connection.connectionPartList:
            print(f"{connection_part.from_.name}->{connection_part.to.name}")
        print(f"Ankunft {connection.arrival}")
