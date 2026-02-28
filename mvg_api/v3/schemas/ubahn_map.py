from __future__ import annotations

from typing import List, Dict, Optional
import logging

from pydantic import BaseModel, RootModel


logger = logging.getLogger("apivis")
logger.setLevel(logging.DEBUG)


class UbahnMapStation(BaseModel):
    """Contains position details of a station to display a network map"""
    name: str
    """Name of the station"""
    id: str
    """IFOPT/global id of the station"""
    efaId: str
    """The divaId/efaId of the station"""
    center_x: Optional[float] = None
    """Center x coordinate of the station"""
    center_y: Optional[float] = None
    """Center y coordinate of the station"""
    label_ax: Optional[float] = None
    """Top left x coordinate of the station label on the svg"""
    label_ay: Optional[float] = None
    """Top left y coordinate of the station label on the svg"""
    label_bx: Optional[float] = None
    """Bottom right x coordinate of the station label on the svg"""
    label_by: Optional[float] = None
    """Bottom right y coordinate of the station label on the svg"""


class UbahnMap(RootModel):
    """A list of ubahn stations with pixel coordinates"""
    root: List[UbahnMapStation]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)


def simplify_api_response(raw_response) -> Dict[str, Dict]:
    """
    Simplifies the rather messy API response to a much flatter json/dict structure such that it can directly be parsed to pydantic objects.
    API response:
    [
        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "layerProperties": {
                            "type": "zoom"
                        },
                        "zoomStation": {
                            "name": "Odeonsplatz",
                            "id": "de:09162:60",
                            "efaId": "60"
                        }
                    },
                    "geometry": {
                        "type": "GeometryCollection",
                        "geometries": [
                            {
                                "type": "Point",
                                "coordinates": [
                                    416.0,
                                    291.0
                                ]
                            },
                            {
                                "type": "MultiPoint",
                                "coordinates": [
                                    [
                                        421.0,
                                        282.0
                                    ],
                                    [
                                        460.0,
                                        288.0
                                    ]
                                ]
                            }
                        ]
                    },
                    "id": ""
                },
                ...
    """

    if len(raw_response) == 0:
        logger.warning("No feature collection served")
        return []
    feature_collection = raw_response[0]
    if "features" not in feature_collection:
        logger.warning("Unexpected feature collection format: no features section")
        return []
    features = feature_collection["features"]
    stations = []
    for feature in features:
        station = {}
        if "properties" in feature and "zoomStation" in feature["properties"]:
            station |= feature["properties"]["zoomStation"]
        else:
            logger.warning("Unexpected feature format: no properties or zoomStation section")
        if "geometry" in feature and "geometries" in feature["geometry"]:
            geometries = feature["geometry"]["geometries"]
            points = [geometry for geometry in geometries if "type" in geometry and geometry["type"] == "Point"]
            multipoints = [geometry for geometry in geometries if "type" in geometry and geometry["type"] == "MultiPoint"]
            if len(points) > 0:
                station["center_x"] = points[0]["coordinates"][0]
                station["center_y"] = points[0]["coordinates"][1]
            else:
                logger.warning("Unexpected geometry format: no points")
            if len(multipoints) > 0:
                station["label_ax"] = multipoints[0]["coordinates"][0][0]
                station["label_ay"] = multipoints[0]["coordinates"][0][1]
                station["label_bx"] = multipoints[0]["coordinates"][1][0]
                station["label_by"] = multipoints[0]["coordinates"][1][1]
            else:
                logger.warning("Unexpected geometry format: no multipoints")
        else:
            logger.warning("Unexpected feature format: no geometry or geometries section")
        stations.append(station)
    return stations
