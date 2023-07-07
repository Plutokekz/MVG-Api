# Unofficial MVG api

An async and sync wrapper for the MVG endpoints, with data validation over pydantic

## Features

- Sync and async support: You can use this wrapper to make API calls synchronously or asynchronously based on your needs.
  It provides flexibility and allows you to leverage the benefits of both approaches.

- Pydantic schema validation: The wrapper integrates with Pydantic, 
 a powerful data validation and parsing library, to validate API responses against
 predefined schemas. This ensures that the received data conforms to the expected structure
 and types.

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

### Example with the old api

```python
from mvg_api.v1.mvg import MVG
mvg = MVG()
mvg.get_location("Hauptbahnhof")
```

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
