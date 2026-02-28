
# Available Endpoints (implemented in v3)

| Description                                  | Function          | API Url                                                        | File                                                |
| -------------------------------------------- | ----------------- | -------------------------------------------------------------- | --------------------------------------------------- |
| PDFs of station plans, maps and timetables   | `get_aushang`     | `.rest/aushang/aushang?id=$mvgId`                              | [aushang.py](mvg_api/v3/schemas/aushang.py)         |
| Connections                                  | `get_connections` | `api/bgw-pt/v3/routes?$params`                                 | [connections.py](mvg_api/v3/schemas/connections.py) |
| Station departures                           | `get_departures`  | `api/bgw-pt/v3/departures?globalId=$stationId`                 | [departures.py](mvg_api/v3/schemas/departures.py)   |
| All MVV lines                                | `get_lines`       | `api/bgw-pt/v3/lines`                                          | [lines.py](mvg_api/v3/schemas/lines.py)             |
| Location search (stations, POIs, streets)    | `get_location`    | `api/bgw-pt/v3/locations?query=$query`                         | [locations.py](mvg_api/v3/schemas/locations.py)     |
| Service Disruptions                          | `get_messages`    | `api/bgw-pt/v3/messages`                                       | [messages.py](mvg_api/v3/schemas/messages.py)       |
| Service Disruptions                          | `get_nearby`      | `api/bgw-pt/v3/stations/nearby`                                | [nearby.py](mvg_api/v3/schemas/nearby.py)           |
| List of all station IDs                      | `get_station_ids` | `.rest/zdm/mvgStationGlobalIds`                                | list[str]                                           |
| Station details                              | `get_station`     | `.rest/zdm/stations/$stationId`                                | [station.py](mvg_api/v3/schemas/station.py)         |
| All MVV+neighboring stations with details    | `get_stations`    | `api/bgw-pt/v3/station`                                        | [stations.py](mvg_api/v3/schemas/stations.py)       |
| Service disruptions                          | `get_ticker`      | `api/ems/tickers`                                              | [ticker.py](mvg_api/v3/schemas/ticker.py)           |
| Map data to position markers (e.g. zoom)     | `get_ubahnmap`    | `.rest/mvgInteractiveImageMap/api/v1/featureCollections/$uuid` | [ubahnmap.py](mvg_api/v3/schemas/ubahnmap.py)       |
| Station zoom info: escalator/elevator status | `get_zoom`        | `.rest/mvgZoom/api/stations/$divaId`                           | [zoom.py](mvg_api/v3/schemas/zoom.py)               |


# Former Endpoints (no longer exist)

| Description                                     | Function                        | API Url                                        |
| ----------------------------------------------- | ------------------------------- | ---------------------------------------------- |
| Key-value information for special lines         | `get_lineinfo`                  | `api/fib/v2/lineinfo`                          |
| Zoom info of a station                          | `get_zoom_station`              | `api/fib/v2/mvgzoomstation/$divaId`            |
| Zoom map canvas without border and info         | `get_plan`                      | `api/fib/v2/mvgzoomstation/$divaId/map`        |
| zoom info of a station, aggregated out of order | `get_zoom_station_out_of_order` | `api/fib/v2/mvgzoomstation/$divaId/outoforder` |
| Nearby vehicles (MVGO)                          | `get_vehicles_in_bounding_box`  | `api/fib/v2/vehicle?$params`                   |
| Surrounding plan of a station                   | `get_surrounding_plan`          | `api/fib/v2/surroundingplan/$mvgId`            |
| Surrounding plans of all stations               | `get_surrounding_plans`         | `api/fib/v2/surroundingplan/$mvgId`            |

# v1 Endpoints

| Description                                         | API Url                    |
| --------------------------------------------------- | -------------------------- |
| Disruption Messages (apparently subset of messages) | `api/ems/slim`             |
| Current Time in milliseconds                        | `clockService/currentDate` |

# Unexplored endpoints

The following endpoints exist and can be found when browsing mvg.de but are not included in the library here.

* TicketingInformation: Information about tickets, prices, etc for a specific connection
  * Endpoint `https://www.mvg.de/api/mtb/v2/mvgde/availableProductss`
  * Example query `https://www.mvg.de/api/mtb/v2/mvgde/availableProducts?language=de&validityBegin=2024-10-07T23:33:54.643Z&itdUnifiedTicketIDs=9999,EINE-M7,EINK,STK-E-9,STK-K-1,STKU21-9,TKS-M7,TKG-M7,TKK,TKF,ICW-M7,ICM-M7,ICMA-M7,ICJA-M7,IC65-M7,IC65MA-M7,IC65JA-M7,AT1W-M7,AT1M-M7,AT2W-M7,AT2M-M7,APC1-M7,APC2-M7,E365J,E365M&traveledZones=ZONE_M-ZONE_7&departureDivaId=990&destinationDivaId=4600`
  * Loaded after a connection was selected in the regular connection search
* ZDMLines
  * Endpoint `https://www.mvg.de/.rest/zdm/zdm-lines`
  * Loaded when displaying messages
  * Loaded alongside the `api/bgw-pt/v3/lines` endpoint, therefore presumably obsolete


# Usage of endpoints on mvg.de

* **Aushang**: _Information about a station_ &rarr; _Infos_ &rarr; _Fahrpläne_ or _Haltestellen- und Umgebungspläne_
* **Connections**: Directly on the homepage mvg.de
* **Departures**: Directly on the homepage mvg.de
* **Lines**
  * When filtering messages, a list of all lines is presented
  * When filtering departures/messages of a specific station, a list of lines for that station is presented
    * _Information about a station_ &rarr; _Abfahrten_ or _Meldungen_ &rarr; _Mehr Filter_
* **Locations**: When searching start and end of a connection or stations for departures
* **Messages**: Directly on the homepage mvg.de
* **Station-Ids**: Unknown
* **Station**: _Information about a station_
* **Stations**: Unknown
* **Ticker**: Unknown
* **Ubahnmap**: Loaded to display aggregated zoom status of all stations on a map in general accessibility page (see below)
* **Zoom**
  * _Information about a station_ &rarr; _Infos_ &rarr; _Infos zu Aufzügen und Rolltreppen_
  * Overview of all stations in general accessibility page (see below)

---

* _Information about a station_
  * Reachable through e.g. _Departures_ from the homepage
  * https://www.mvg.de/meinhalt/sendlinger-tor
* Zoom overview: https://www.mvg.de/ueber-die-mvg/unser-engagement/barrierefreiheit/zoom.html

