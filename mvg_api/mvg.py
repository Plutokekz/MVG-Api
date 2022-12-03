from Levenshtein import ratio

from mvg_api.api.api import Api
from mvg_api.models.route import Location, LocationType


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

    def get_rout(self, location_from, location_to):
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
        return self.api.get_route(location_from, location_to)


if __name__ == "__main__":
    mvg = MVG()
    for connection in mvg.get_rout("Holzkirchen", "Garching").connectionList:
        print(f"Von {connection.from_.name} nach {connection.to.name}")
        print(f"Abfahrt {connection.arrival - connection.departure}")
        for connection_part in connection.connectionPartList:
            print(f"{connection_part.from_.name}->{connection_part.to.name}")
        print(f"Ankunft {connection.arrival}")
