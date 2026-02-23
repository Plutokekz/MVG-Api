
# Available Endpoints

| Description                                     | Function                                     | API Url                                        | File                                                |
| ----------------------------------------------- | -------------------------------------------- | ---------------------------------------------- | --------------------------------------------------- |
| PDFs of station plans, maps and timetables      | [`get_aushang`](#method-get_aushang)         | `.rest/aushang/aushang?id=$mvgId`              | [aushang.py](mvg_api/v3/schemas/aushang.py)         |
| Connections                                     | [`get_connections`](#method-get_connection)  | `api/bgw-pt/v3/routes?$params`                 | [connections.py](mvg_api/v3/schemas/connections.py) |
| Station departures                              | [`get_departures`](#method-get_departures)   | `api/bgw-pt/v3/departures?globalId=$stationId` | [departures.py](mvg_api/v3/schemas/departures.py)   |
| All MVV lines                                   | [`get_lines`](#method-get_lines)             | `api/bgw-pt/v3/lines`                          | [lines.py](mvg_api/v2/schemas/lines.py)             |
| Location search (stations, POIs, streets)       | [`get_location`](#method-get_location)       | `api/bgw-pt/v3/locations?query=$query`         | [locations.py](mvg_api/v2/schemas/locations.py)     |
| Service Disruptions (stations and publish date) | [`get_messages`](#method-get_messages)       | `api/bgw-pt/v3/messages`                       | [messages.py](mvg_api/v2/schemas/messages.py)       |
| List of all station IDs                         | [`get_station_ids`](#method-get_station_ids) | `.rest/zdm/mvgStationGlobalIds`                | list[str]                                           |
| Station details                                 | [`get_station`](#method-get_station)         | `.rest/zdm/stations/$stationId`                | [station.py](mvg_api/v2/schemas/station.py)         |
| All MVV+neighboring stations with details       | [`get_stations`](#method-get_stations)       | `api/bgw-pt/v3/station`                        | [stations.py](mvg_api/v2/schemas/stations.py)       |
| Service disruptions                             | [`get_ticker`](#method-get_ticker)           | `api/ems/tickers`                              | [ticker.py](mvg_api/v2/schemas/ticker.py)           |
| Station zoom info: escalator/elevator status    | [`get_zoom`](#method-get_zoom)               | `.rest/mvgZoom/api/stations/$divaId`           | [zoom.py](mvg_api/v2/schemas/zoom.py)               |
| Zoom overview of all stations                   | [`get_zoom_overview`](#method-get_zoom)      | `.rest/mvgZoom/api/stations`                   | [zoom.py](mvg_api/v2/schemas/zoom.py)               |


# Former Endpoints

| Description                                     | Function                        | API Url                                        |
| ----------------------------------------------- | ------------------------------- | ---------------------------------------------- |
| Key-value information for special lines         | `get_lineinfo`                  | `api/fib/v2/lineinfo`                          |
| Zoom info of a station                          | `get_zoom_station`              | `api/fib/v2/mvgzoomstation/$divaId`            |
| Zoom map canvas without border and info         | `get_plan`                      | `api/fib/v2/mvgzoomstation/$divaId/map`        |
| zoom info of a station, aggregated out of order | `get_zoom_station_out_of_order` | `api/fib/v2/mvgzoomstation/$divaId/outoforder` |
| Nearby vehicles (MVGO)                          | `get_vehicles_in_bounding_box`  | `api/fib/v2/vehicle?$params`                   |
| Surrounding plan of a station                   | `get_surrounding_plan`          | `api/fib/v2/surroundingplan/$mvgId`            |
| Surrounding plans of all stations               | `get_surrounding_plans`         | `api/fib/v2/surroundingplan/$mvgId`            |


# Unexplored endpoints

The following endpoints exist and can be found when browsing mvg.de but are not included in the library here.

* TicketingInformation: Information about tickets, prices, etc for a specific connection
  * Endpoint `https://www.mvg.de/api/mtb/v2/mvgde/availableProductss`
  * Example query `https://www.mvg.de/api/mtb/v2/mvgde/availableProducts?language=de&validityBegin=2024-10-07T23:33:54.643Z&itdUnifiedTicketIDs=9999,EINE-M7,EINK,STK-E-9,STK-K-1,STKU21-9,TKS-M7,TKG-M7,TKK,TKF,ICW-M7,ICM-M7,ICMA-M7,ICJA-M7,IC65-M7,IC65MA-M7,IC65JA-M7,AT1W-M7,AT1M-M7,AT2W-M7,AT2M-M7,APC1-M7,APC2-M7,E365J,E365M&traveledZones=ZONE_M-ZONE_7&departureDivaId=990&destinationDivaId=4600`
  * Loaded after a connection was selected in the regular connection search
* ZoomOverviewInteractive: Zoom overview of whole ubahn network
  * Endpoint `https://www.mvg.de/.rest/mvgInteractiveImageMap/api/v1/featureCollections/a5ac8f68-1f4a-45c0-acc2-7cbdb3740f58`
  * UUID appears to be constant
  * Encodes position information of stations on a map
  * Loaded from the general MVG accessibility information site https://www.mvg.de/ueber-die-mvg/unser-engagement/barrierefreiheit/zoom.html
  * Loaded alongside `.rest/mvgZoom/api/stations`, therefore presumably obsolete
* ZDMLines
  * Endpoint `https://www.mvg.de/.rest/zdm/zdm-lines`
  * Loaded when displaying messages
  * Loaded alongside the `api/bgw-pt/v3/lines` endpoint, therefore presumably obsolete


# Where to find these endpoints

* Aushang
  * Information about a station &rarr; _Infos_ &rarr; _Fahrpläne_ or _Haltestellen- und Umgebungspläne_
* Connections
  * Directly on the homepage mvg.de
* Departures
  * Directly on the homepage mvg.de
* Lines
  * When filtering messages, a list of all lines is presented
  * When filtering departures/messages of a specific station, a list of lines for that station is presented
    * Information about a station &rarr; _Abfahrten_ or _Meldungen_ &rarr; _Mehr Filter_
* Locations
  * When searching start and end of a connection or stations for departures
* Messages
  * Directly on the homepage mvg.de
* Station-Ids
  * Unknown
* Station
  * Information about a station
* Stations
  * Unknown
* Ticker
  * Unknown
* Zoom
  * Information about a station &rarr; _Infos_ &rarr; _Infos zu Aufzügen und Rolltreppen_

---

* Information about a station
  * Reachable through e.g. _Departures_ from the homepage
  * https://www.mvg.de/meinhalt/sendlinger-tor

