from typing import Dict, Any, Optional, List

import httpx

from mvg_api.v3.schemas.location import LocationType


class RequestFailed(Exception):
    """
    Exception when a request to the MVG api was not successful for any reason.
    """


class MVGRequests:
    url: str = "https://www.mvg.de/"

    @staticmethod
    def aushang(headers: Dict[str, str], plan_id: str) -> httpx.Request:
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}.rest/aushang/stations",
            headers=headers,
            params={"id": plan_id},
        )

    @staticmethod
    def connections(
        headers: Dict[str, str],
        origin_station_id: str,
        destination_station_id: str,
        routing_date_time: str,
        *,
        routing_date_time_is_arrival: bool = None,
        transport_types: Optional[str] = None,
        route_type: Optional[str] = None,
        change_speed: Optional[str] = None,
        accessibility_options: Optional[str] = None,
        via_station_id: Optional[str] = None,
        via_dwell_time_minutes: Optional[int] = None,
        origin_latitude: Optional[float] = None,
        origin_longitude: Optional[float] = None,
        destination_latitude: Optional[float] = None,
        destination_longitude: Optional[float] = None
    ) -> httpx.Request:
        param = httpx.QueryParams(
            {
                "originStationGlobalId": origin_station_id,
                "destinationStationGlobalId": destination_station_id,
                "routingDateTime": routing_date_time,
                "routingDateTimeIsArrival": routing_date_time_is_arrival,
                "transportTypes": transport_types,
                "routeType": route_type,
                "changeSpeed": change_speed,
                "accessibilityOptions": accessibility_options,
                "viaStationGlobalId": via_station_id,
                "viaDwellTimeInMinutes": via_dwell_time_minutes,
                "originLatitude": origin_latitude,
                "originLongitude": origin_longitude,
                "destinationLatitude": destination_latitude,
                "destinationLongitude": destination_longitude,
            }
        )
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/bgw-pt/v3/routes",
            params=param,
            headers=headers,
        )

    @staticmethod
    def departures(
        headers: Dict[str, str],
        station_id: str,
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
            f"{MVGRequests.url}api/bgw-pt/v3/departures",
            params=param,
            headers=headers,
        )

    @staticmethod
    def lines(headers: Dict[str, str], station_id: Optional[str]):
        url = f"{MVGRequests.url}api/bgw-pt/v3/lines/{station_id}"
        if station_id is None:
            url = f"{MVGRequests.url}api/bgw-pt/v3/lines"
        return httpx.Request(
            "GET", url, headers=headers
        )

    @staticmethod
    def locations(
        headers: Dict[str, str],
        query: str,
        limit_address_poi: int,
        limit_stations: int,
        location_types: List[LocationType],
    ) -> httpx.Request:
        param = httpx.QueryParams(
            {
                "query": query,
                "limitAddressPoi": limit_address_poi,
                "limitStations": limit_stations,
                "locationTypes": (
                    ",".join([x.value for x in location_types])
                    if location_types is not None
                    else None
                ),
            }
        )
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/bgw-pt/v3/locations",
            params=param,
            headers=headers,
        )

    @staticmethod
    def messages(headers: Dict[str, str], message_type: Optional[str] = None) -> httpx.Request:
        param = httpx.QueryParams({"messageType": message_type})
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/bgw-pt/v3/messages",
            params=param,
            headers=headers,
        )

    @staticmethod
    def nearby(headers: Dict[str, str], latitude: float, longitude: float) -> httpx.Request:
        param = httpx.QueryParams({"latitude": latitude, "longitude": longitude})
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}api/bgw-pt/v3/stations/nearby",
            params=param,
            headers=headers,
        )

    @staticmethod
    def station_ids(headers: Dict[str, str]) -> httpx.Request:
        return httpx.Request(
            "GET", f"{MVGRequests.url}.rest/zdm/mvgStationGlobalIds", headers=headers
        )

    @staticmethod
    def station(headers: Dict[str, str], station_id: str) -> httpx.Request:
        return httpx.Request(
            "GET", f"{MVGRequests.url}.rest/zdm/stations/{station_id}", headers=headers
        )

    @staticmethod
    def stations(
        headers: Dict[str, str], hash_: Optional[str], world: Optional[bool]
    ) -> httpx.Request:
        param = httpx.QueryParams({"hash": hash_, "world": world})
        return httpx.Request(
            "GET", f"{MVGRequests.url}api/bgw-pt/v3/stations", headers=headers, params=param
        )

    @staticmethod
    def ticker(headers: Dict[str, str]) -> httpx.Request:
        return httpx.Request(
            "GET", f"{MVGRequests.url}api/ems/tickers", headers=headers
        )

    @staticmethod
    def ubahn_map(headers: Dict[str, str], uuid: str = "a5ac8f68-1f4a-45c0-acc2-7cbdb3740f58") -> httpx.Request:
        return httpx.Request(
            "GET",
            f"{MVGRequests.url}.rest/mvgInteractiveImageMap/api/v1/featureCollections/{uuid}",
            headers=headers,
        )

    @staticmethod
    def zoom(headers: Dict[str, str], efa_id: Optional[str] = None) -> httpx.Request:
        url = f"{MVGRequests.url}.rest/mvgZoom/api/stations/{efa_id}"
        if efa_id is None:
            url = f"{MVGRequests.url}.rest/mvgZoom/api/stations"
        return httpx.Request("GET", url, headers=headers,)
