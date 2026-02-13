# sync and async api are identical except for async/await keywords
# use the following command to quickly generate the sync variant from the async variant when functions were changed
#
# echo "# DO NOT EDIT - DERIVED FROM asyncapi.py" > syncapi.py && sed -e 's/async def/def/g' -e 's/= await/=/g' -e 's/AsyncApi/SyncApi/g' -e 's/AsyncClient/Client/g' asyncapi.py >> syncapi.py


import json
from typing import Dict, Any, Optional, List
from .requests import MVGRequests, RequestFailed

import httpx

from mvg_api.v3.schemas import (
    ems,
    station,
    transportdevice,
    aushang,
)
from mvg_api.v3.schemas.location import LocationType


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

    async def get_aushang(self, plan_id: str) -> aushang.Aushaenge:
        """
        Get the aushang for a station, get all Playn that a currently active in a stations blackboard.
        :param plan_id: I am not sure bit it seems to be the first 2 letters of the station name in uppercase.
         For example
        KA for Karlsplatz
        :return: a list of aushaenge
        """
        response = await self._send_request(MVGRequests.aushang(self.headers, plan_id))
        return aushang.Aushaenge(response)

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

    async def get_station_ids(self) -> List[str]:
        """
        Get all the station ids
        :return: returns a list of strings with all the station ids that are available
        """
        response = await self._send_request(MVGRequests.station_ids(self.headers))
        return list(response)
