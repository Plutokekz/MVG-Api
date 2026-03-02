# Unofficial MVG api

An async and sync wrapper for the MVG endpoints, with data validation through pydantic.

## Features

* **Fully :tm: complete**: There is a wrapper for all endpoints known and/or currently used by the mvg.de homepage as of early 2026 in the **mvg_api.v3** interface.
  See the [functions](#functions) section for the available endpoints.
* **Sync and async support**: You can use this wrapper to make API calls synchronously or asynchronously based on your needs.
  It provides flexibility and allows you to leverage the benefits of both approaches.
* **Pydantic schema validation**: The wrapper integrates with pydantic, a powerful data validation and parsing library, to validate API responses against
 predefined schemas.
 This ensures that the received data conforms to the expected structure and types.
 For every API endpoint, there is a corresponding pydantic schema that defines the expected structure of the response.
 If the response does not match the schema, an exception is raised.
* **Documented schemas**: All schemas are documented with the known (or assumed) result type and content to that you know what data you can expect.
* **Common line representation**: The api itself is not very consistent in attribute naming, especially with lines/services. To simplify handling and displayal of lines the helper class `NetworkLine` provides unified access to the lines returned by the departure, connection, aushang, ... endpoints.
  The helper can also provides color codes for the individual lines.


## Installation

Install it over pip or from source by cloning the repository and installing the dependencies with [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
pip install async-mvg-api
```

or

```bash
git clone https://github.com/Plutokekz/MVG-Api.git
cd MVG-Api
uv sync
```

## Usage

```python
from mvg_api.v3 import SyncMVG

# load station information of 'Sendlinger Tor'
station_info = SyncMVG().get_station("de:09162:50")
print(station_info)

# load departures at 'Sendlinger Tor'
departures = SyncMVG().get_departures("de:09162:50")
print(departures)
```

The station info will yield:

```json
{
  "name": "Sendlinger Tor",
  "place": "München",
  "id": "de:09162:50",
  "divaId": 50,
  "abbreviation": "SE",
  "tariffZones": "m",
  "products": [
    "UBAHN",
    "TRAM",
    "BUS"
  ],
  "latitude": 48.133444,
  "longitude": 11.566681
}
```

See the list of functions below for the other available endpoints.


### Functions

All functions and schemas are documented.

| Description                                  | Function          |
| -------------------------------------------- | ----------------- |
| PDFs of station plans, maps and timetables   | `get_aushang`     |
| Connections                                  | `get_connections` |
| Station departures                           | `get_departures`  |
| All MVV lines                                | `get_lines`       |
| Location search (stations, POIs, streets)    | `get_location`    |
| Service Disruptions                          | `get_messages`    |
| Nearby stations                              | `get_nearby`      |
| List of all station IDs                      | `get_station_ids` |
| Station details                              | `get_station`     |
| All MVV+neighboring stations with details    | `get_stations`    |
| Service disruptions                          | `get_ticker`      |
| Map data to position markers (e.g. zoom)     | `get_ubahnmap`    |
| Station zoom info: escalator/elevator status | `get_zoom`        |


### Something not working?

There is quite some development in the api by mvg.de, leading to semi-frequent breaking changes or new attributes that are available.
The latest breaking change was from `fib/v2` to `bgw-pt/v3` in October of 2024.

If a response does not match the pydantic schema, an exception is raised.
If that is the case, you can hotfix the schema directly.
In most cases that will be a required attribute that is no longer returned by the api.
Please also file an issue on this repository such that it can be fixed soon in the library.


### Clarification on station ids

There are multiple different identifiers used for stations in the MVV and MVG areas

| ID                | Description                                      | Karlsplatz | Sendlinger Tor |
| ----------------- | ------------------------------------------------ | ---------- | -------------- |
| MVG id            | 2-3 capital letters, identifying stations of MVG | KA         | SE (and SU)    |
| Global/Station id | IFOPT stop id; global identification             | de:09162:1 | de:09162:50    |
| Diva/Efa id       | Station part of the IFOPT id                     | 1          | 50             |

[IFOPT](https://wiki.openstreetmap.org/wiki/Key:ref:IFOPT) stop ids are in the format `country:admin_area:stop_place[:level:quay]` (aka `country:region:station[:stopgroup:stoppoint]`).

Stop points of a station have a more detailed IFOPT id with the suffix :stopgroup:stoppoint.
For ubahn services, the stopgroup identifies the Bahnsteig (e.g. only one at Universität, but two at Innsbrucker Ring) and the stopoint identifies the track and is typically offset by 50 (e.g. track 1 is :51).


### Clarification on line ids

Among others, there is also a diva id to identify lines (not to be confused with the station diva id):  
Encountered '92M07' for S7, '92M01' for S1, '010U6' for U6, '' for fussweg


## Tests

```bash
uv run pytest mvg_api/v1/tests/api_tests.py mvg_api/v2/tests/api_tests.py mvg_api/v3/tests/api_tests.py
```


# Credit

For Endpoint Information and Code snippets
* https://github.com/leftshift/python_mvg_api
* https://www.mvg.de/


# Usage policy of the MVG api

> ACHTUNG:
>
> Unsere Systeme dienen der direkten Kundeninteraktion. Die Verarbeitung unserer Inhalte oder Daten durch Dritte erfordert unsere ausdrückliche Zustimmung. Für private, nicht-kommerzielle Zwecke, wird eine gemäßigte Nutzung ohne unsere ausdrückliche Zustimmung geduldet. Jegliche Form von Data-Mining stellt keine gemäßigte Nutzung dar. Wir behalten uns vor, die Duldung grundsätzlich oder in Einzelfällen zu widerrufen. Fragen richten Sie bitte gerne an: redaktion@mvg.de.

In other words: Private, noncommercial, moderate use of the API is tolerated.
They do not consider data mining as a moderate use.

(Disclaimer: I am not a lawyer, this is not legal advice)
