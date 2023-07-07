# Unofficial MVG api

An async and sync wrapper for the MVG endpoints, with data validation over pydantic

## Features

- Sync and async support: You can use this wrapper to make API calls synchronously or asynchronously based on your needs.
  It provides flexibility and allows you to leverage the benefits of both approaches.

- Pydantic schema validation: The wrapper integrates with Pydantic, 
 a powerful data validation and parsing library, to validate API responses against
 predefined schemas. This ensures that the received data conforms to the expected structure
 and types. For every API endpoint, there is a corresponding Pydantic schema that defines the expected structure of the
 response. If the response does not match the schema, an exception is raised. **And you allways know what data you get**.

## Installation
Install it over pip or from source by cloning the repository and installing 
the dependencies with [poetry](https://python-poetry.org/).

```bash
pip install async-mvg-api
```

or 

```bash
git clone https://github.com/Plutokekz/MVG-Api.git
cd MVG-Api
poetry install
```
## Usage

With the endpoint changes from MVG the api is now split into versions. Currently, there are two versions available.
The first version is the old api, which is still available and work, but I think in the future it may stop working 
and will be removed.

The second version is the new api, which is still in beta, should work until MVG changes there endpoints one again. 
### Example with the v2 api

#### Sync
```python
from mvg_api.v2.mvg import SyncMVG
mvg = SyncMVG()
location = mvg.get_location("Hauptbahnhof")
```
#### Async
```python
from mvg_api.v2.mvg import AsyncMVG
import asyncio
mvg = AsyncMVG()
location = asyncio.run(mvg.get_location("Hauptbahnhof"))
```

the location from sync and async should look somthing like this:

```python
LocationList(
    locations=[
        Location(
            globalId='de:09162:6',
            type=<LocationType.STATION: 'STATION'>,
            latitude=48.14003,
            longitude=11.56107,
            divaId=6,
            place='München',
            name='Hauptbahnhof',
            hasZoomData=True,
            tariffZones='m',
            aliases='Hbf München main station central station Muenchen Munchen HU HO HUHO',
            transportTypes=[
                'UBAHN',
                'TRAM',
                'SBAHN'
                ],
            surroundingPlanLink='HU'
            ),
            ...
        ]
    )
```

### Example with the v1 api

#### Sync
```python
from mvg_api.v1.mvg import MVG
mvg = MVG()
location = mvg.get_location("Hauptbahnhof")
```
#### Async
```python
from mvg_api.v1.mvg import AsyncMVG
import asyncio
mvg = AsyncMVG()
location = asyncio.run(mvg.get_location("Hauptbahnhof"))
```

the location from sync and async should look somthing like this:

```python
LocationList(
    locations=[
        Location(
            globalId='de:09162:6',
            type=<LocationType.STATION: 'STATION'>,
            latitude=48.14003,
            longitude=11.56107,
            divaId=6,
            place='München',
            name='Hauptbahnhof',
            hasZoomData=True,
            tariffZones='m',
            aliases='Hbf München main station central station Muenchen Munchen HU HO HUHO',
            transportTypes=[
                'UBAHN',
                'TRAM',
                'SBAHN'
                ],
            surroundingPlanLink='HU'
            ),
            ...
        ]
    )
```

## Documentation of v2 endpoints
### Endpoints

#### Method: get_departures_by_name

```python
def get_departures_by_name(self, name: str, **kwargs) -> departure.Departures
```

Get the departures for a given station name, the keyword arguments are the same as in get_departures

- Parameters:
    - `name`: Name of the Station.
    - `**kwargs`: Keyword arguments for the get_departures method.
- Returns a `departure.Departures` object representing the Departures information.

#### Method: get_connection_by_name

````python
def get_connection_by_name(self, start: str, stop: str, start_datetime: Optional[datetime.datetime] = None,
                           date_time_is_arrival: bool = False, **kwargs) -> Connections:
````

Get a connection between two locations by the station or address name, the keyword arguments are the same as in
get_connection

- Parameters:
    - `start`: the start location/ address name
    - `stop`: the stop location/ address name
    - `start_datetime`: the start datetime of the connection
    - `date_time_is_arrival`: if the start_datetime is the arrival time
    - `**kwargs`: Keyword arguments for the get_connection method.
- Returns a `connection.Connections` object representing the connection information.

#### Method: get_ticker

```python
def get_ticker(self) -> ems.Messages
```
Get ticker messages, updates about the disruptions and planed works on the MVG train network 
There 2 types of messages DISRUPTION and PLANNED
- Returns a list of ticker messages containing updates about disruptions and planned works on the MVG train network.

#### Method: get_station

```python
def get_station(self, station_id: str) -> station.Station
```

Get a station by its id the Station id can be found in the get_all_stations list, or it can be obtained from a
location method wenn the found Location is of the type STATION

- Parameters:
  - `station_id`: The ID of the station.
- Returns a `station.Station` object representing the station information.

#### Method: get_departures

```python
def get_departures(
    self,
    station_id: str,
    *,
    limit: Optional[int] = None,
    offset_minutes: Optional[int] = None,
    transport_types: Optional[Any] = None,
    language: Optional[str] = None,
) -> departure.Departures
```
Get the departures for a station
- Parameters:
  - `station_id`: the same id as in get_station, for example de:09162:6 for Hauptbahnhof, and it can be
        obtained
        from a location method wenn the found Location is of the type STATION or from the get_all_stations method
  - `limit` (optional): The maximum number of departures to return.
  - `offset_minutes` (optional): The offset in minutes from the current time for the departures.
  - `transport_types` (optional): A list of specific transport types to filter the departures (e.g., UBAHN, TRAM, BUS).
  - `language` (optional): the language ? I have no idea why this is here maybe for the language in the response. But I
        didn't see any difference when I changed it
- Returns a `departure.Departures` object representing the list of departures.

#### Method: get_escalators_and_elevators

```python
def get_escalators_and_elevators(self, efa_id: int) -> transportdevice.StationTransportDevices
```
Get the escalators and elevators location and status for a station
- Parameters:
  - `efa_id`: an integer number that is associated with a station. It is included in the Station object but
        under the name of divId for some reason.
- Returns a `transportdevice.StationTransportDevices` object representing the escalators and elevators at the station.

#### Method: get_aushang

```python
def get_aushang(self, plan_id: str) -> aushang.Aushaenge
```
Get the aushang for a station, get all Playn that a currently active in a stations blackboard.
- Parameters:
  - `plan_id`: I am not sure bit it seems to be the first 2 letters of the station name in uppercase.
         For example KA for Karlsplatz
- Returns a `aushang.Aushaenge` object representing the aushang (playn) currently active at the station.

#### Method: get_station_ids

```python
def get_station_ids(self) -> List[str]
```
Get all the station ids
- Returns a list of all station IDs available.

#### Method: get_location

```python
def get_location(
    self,
    query: str,
    limit_address_poi: Optional[int] = None,
    limit_stations: Optional[int] = None,
    location_types: Optional[List[LocationType]] = None,
) -> location.Locations
```
Get the location of a query, it can be a station name or a street name or a POI
- Parameters:
  - `query`: The address, station name, or POI name to search for.
  - `limit_address_poi` (optional): Limit the number of addresses or POIs to return.
  - `limit_stations` (optional): Limit the number of stations to return.
  - `location_types` (optional): Limit the location types to return (e.g., STATION, POI, ADDRESS).
- Returns a `location.Locations` object representing the list of locations.

#### Method: get_messages

```python
def get_messages(self, message_type: Optional[str] = None) -> messages.Messages
```
Get the messages from the message board. Somehow similar to the ems ticker but it has more and different
information.

- Parameters:
  - `message_type` (optional): The type of message to retrieve (e.g., INCIDENT, SCHEDULE_CHANGE).
- Returns a `messages.Messages` object representing the list of messages from the message board.

#### Method: get_connection

```python
def get_connection(
    self,
    origin_station_id: str,
    destination_station_id: str,
    routing_date_time: str,
    *,
    routing_date_time_is_arrival: bool,
    transport_types: Optional[str] = None,
    origin_latitude: Optional[float] = None,
    origin_longitude: Optional[float] = None,
    destination_latitude: Optional[float] = None,
    destination_longitude: Optional[float] = None,
) -> connection.Connections
```
Get the connections between two stations or coordinates.
You can use either station_id to station_id or coordinates to coordinates or station_id to coordinates.
- Parameters:
  - `origin_station_id`: The ID of the origin station.
  - `destination_station_id`: The ID of the destination station.
  - `routing_date_time`: The date and time of the departure or arrival.
  - `routing_date_time_is_arrival`: Specifies if `routing_date_time` is the arrival time.
  - `transport_types` (optional): the transport types to use, available types are SCHIFF,RUFTAXI,BAHN,UBAHN,TRAM,SBAHN,BUS
        ,REGIONAL_BUS
  - `origin_latitude` (optional): The latitude of the origin station.
  - `origin_longitude` (optional): The longitude of the origin station.
  - `destination_latitude` (optional): The latitude of the destination station.
  - `destination_longitude` (optional): The longitude of the destination station.
- Returns a `connection.Connections` object representing the list of connections between the origin and destination.

#### Method: get_lineinfo

```python
def get_lineinfo(self, language: Optional[str]) -> lineinfo.Infos
```
Get the line info for some wired special lines like "lufthanse express bus"
- Parameters:
  - `language` (optional):  here the language argument also makes no difference in the response output.
- Returns a `lineinfo.Infos` object representing the line information for special lines.

#### Method: get_stations

```python
def get_stations(
    self, hash_: Optional[str] = None, world: Optional[bool] = None
) -> stations.Locations
```
Get all the stations, like get_station_ids but with the hole station information.
- Parameters:
  - `hash_` (optional):I don't know for what this hash is. (In the response is a hash, but if you send it again you get
        no response, so keep it empty)
  - `world` (optional): you can set the world to true or false. Maybe some day the MVG is operating worldwide.
- Returns a `stations.Locations` object representing the list of stations.

#### Method: get_lines

```python
def get_lines(self) -> line.Lines
```
Get all the lines
- Returns a `line.Lines` object representing the list of lines.

#### Method: get_zoom_station

```python
def get_zoom_station(self, div_id: int) -> zoom_station.ZoomStation
```
Get information about the availability TransportDevices at a station. Like elevators, escalators, etc.
The information if similar to the information you get from the get_escalators_and_elevators
- Parameters:
  - `div_id`: An internal number associated with a station.
- Returns a `zoom_station.ZoomStation` object representing information about the availability of transport devices at a station.

#### Method: get_plan

```python
def get_plan(self, div_id: int) -> bytes
```
Get the plan of a station. The response is a pdf file in bytes.
- Parameters:
  - `div_id`: An internal number associated with a station.
- Returns the plan of a station as a byte array (PDF format).

#### Method: get_zoom_station_out_of_order

```python
def get_zoom_station_out_of_order(self, div_id: int) -> out_of_order.StationOutOfOrder
```
Get the information about the availability of TransportDevices at a station. Like elevators, escalators, etc.
- Parameters:
  - `div_id`: An internal number associated with a station.
- Returns a `out_of_order.StationOutOfOrder

object representing the information about the availability of transport devices at a station.

#### Method: get_vehicles_in_bounding_box

```python
def get_vehicles_in_bounding_box(
    self, bbswlat: float, bbswlng: float, bbnelat: float, bbnelng: float
) -> vehicel.VehiclesAndSharingStations
```
Get the vehicles and sharing stations in a bounding box. The bounding box is defined by two coordinates.
- Parameters:
  - `bbswlat`: The latitude of the bounding box's southwest corner.
  - `bbswlng`: The longitude of the bounding box's southwest corner.
  - `bbnelat`: The latitude of the bounding box's northeast corner.
  - `bbnelng`: The longitude of the bounding box's northeast corner.
- Returns a `vehicel.VehiclesAndSharingStations` object representing the vehicles and sharing stations within the specified bounding box.

#### Method: get_surrounding_plan

```python
def get_surrounding_plan(
    self, plan_id: str, world: bool = True, include_image_data: bool = True
) -> surounding_plans.Plan
```
Get the surrounding plan of a station. If you include the image data you get a base64 encoded pdf of the plan.
        So you have to decode it first.
- Parameters:
  - `plan_id`: the first 2 letters of the station name in uppercase. For example "KA" for Karlsplatz
  - `world` (optional): again a world argument, but it makes no difference in the response output.
  - `include_image_data` (optional): A boolean value specifying if the response should include the image data of the plan.
- Returns a `surounding_plans.Plan` object representing the surrounding plan of a station.

#### Method: get_surrounding_plans

```python
def get_surrounding_plans(self, world: Optional[bool] = True) -> surounding_plans.Plans
```
Get the surrounding plan of a station. If you include the image data you get a base64 encoded pdf of the plan.
So you have to decode it first.
- Parameters:
  - `world` (optional): again a world argument, but it makes no difference in the response output.
- Returns a `surounding_plans.Plans` object representing the list of surrounding plans for all stations.


## Tests

```bash
poetry run pytest mvg_api/v1/tests/api_tests.py mvg_api/v2/tests/api_tests.py
```

# Credit
For Endpoint Information and Code snippets
* https://github.com/leftshift/python_mvg_api
* https://www.mvg.de/

# Usage policy of the MVG api
## ACHTUNG:
Unsere Systeme dienen der direkten Kundeninteraktion. Die Verarbeitung unserer Inhalte oder Daten durch Dritte erfordert unsere ausdrückliche Zustimmung. Für private, nicht-kommerzielle Zwecke, wird eine gemäßigte Nutzung ohne unsere ausdrückliche Zustimmung geduldet. Jegliche Form von Data-Mining stellt keine gemäßigte Nutzung dar. Wir behalten uns vor, die Duldung grundsätzlich oder in Einzelfällen zu widerrufen. Fragen richten Sie bitte gerne an: redaktion@mvg.de.

In other words: Private, noncomercial, moderate use of the API is tolerated. They don't consider data mining as moderate use.

(Disclaimer: I am not a lawyer, this isn't legal advice)
