# Unofficial MVG api

An async and sync wrapper for the MVG endpoints, with data validation over pydantic

## Breaking Changes

**MVG changed the api again. Currently only a few endpoints work in v1 and v2.** 

between version 0.1.5 and 0.2.0 the api has changed a lot. The api is now split into versions.
The old api is available under mvg_api.v1 and the new api is available under mvg_api.v2.

## Features

- Sync and async support: You can use this wrapper to make API calls synchronously or asynchronously based on your needs.
  It provides flexibility and allows you to leverage the benefits of both approaches.

- Pydantic schema validation: The wrapper integrates with Pydantic, 
 a powerful data validation and parsing library, to validate API responses against
 predefined schemas. This ensures that the received data conforms to the expected structure
 and types. For every API endpoint, there is a corresponding Pydantic schema that defines the expected structure of the
 response. If the response does not match the schema, an exception is raised. **And you always know what data you get**.

## Installation
Install it over pip or from source by cloning the repository and installing 
the dependencies with [uv](https://docs.astral.sh/uv/getting-started/installation/).

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

With the endpoint changes from MVG the api is now split into versions. Currently, there are two versions available.
The first version is the old api, which is still available and works, but I think in the future it may stop working 
and will be removed.

The second version is the new api, which is still in beta, should work until MVG changes their endpoints one again.

## Documentation of v2 endpoints

### Endpoints

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
location method when the found Location is of the type STATION

- Parameters:
  - `station_id`: The ID of the station.
- Returns a `station.Station` object representing the station information.

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
Get the aushang for a station, get all Playn that a currently active in a stations' blackboard.
- Parameters:
  - `plan_id`: I am not sure bit it seems to be the first 2 letters of the station name in uppercase.
         For example, KA for Karlsplatz
- Returns a `aushang.Aushaenge` object representing the aushang (playn) currently active at the station.

#### Method: get_station_ids

```python
def get_station_ids(self) -> List[str]
```
Get all the station ids
- Returns a list of all station IDs available.

## Tests

```bash
uv run pytest mvg_api/v1/tests/api_tests.py mvg_api/v2/tests/api_tests.py
```

# Credit
For Endpoint Information and Code snippets
* https://github.com/leftshift/python_mvg_api
* https://www.mvg.de/

# Usage policy of the MVG api
## ACHTUNG:
Unsere Systeme dienen der direkten Kundeninteraktion. Die Verarbeitung unserer Inhalte oder Daten durch Dritte erfordert unsere ausdrückliche Zustimmung. Für private, nicht-kommerzielle Zwecke, wird eine gemäßigte Nutzung ohne unsere ausdrückliche Zustimmung geduldet. Jegliche Form von Data-Mining stellt keine gemäßigte Nutzung dar. Wir behalten uns vor, die Duldung grundsätzlich oder in Einzelfällen zu widerrufen. Fragen richten Sie bitte gerne an: redaktion@mvg.de.

In other words: Private, noncommercial, moderate use of the API is tolerated.
They do not consider data mining as a moderate use.

(Disclaimer: I am not a lawyer, this is not legal advice)
