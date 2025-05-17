import datetime
from typing import List

from mvg_api.v1.api import Api, AsyncApi
from mvg_api.v1.schemas.ticker import TickerList, SlimList


class MVG:
    api: Api

    def __init__(self):
        self.api = Api()

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


class AsyncMVG:
    api: AsyncApi

    def __init__(self):
        self.api = AsyncApi()

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
