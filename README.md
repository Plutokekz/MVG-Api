# Unofficial MVG api

An async and sync wrapper for the MVG endpoints, with data validation over pydantic

# Usage policy of the MVG api
## ACHTUNG: 
Unsere Systeme dienen der direkten Kundeninteraktion. Die Verarbeitung unserer Inhalte oder Daten durch Dritte erfordert unsere ausdrückliche Zustimmung. Für private, nicht-kommerzielle Zwecke, wird eine gemäßigte Nutzung ohne unsere ausdrückliche Zustimmung geduldet. Jegliche Form von Data-Mining stellt keine gemäßigte Nutzung dar. Wir behalten uns vor, die Duldung grundsätzlich oder in Einzelfällen zu widerrufen. Fragen richten Sie bitte gerne an: redaktion@mvg.de.

In other words: Private, noncomercial, moderate use of the API is tolerated. They don't consider data mining as moderate use.

(Disclaimer: I am not a lawyer, this isn't legal advice)

## Installation
pip installation or clone the repository and install the [poetry](https://python-poetry.org/) dependencies

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

```python
from mvg_api.mvg import MVG
mvg = MVG()
mvg.get_location("Hauptbahnhof")
```

## Tests

```bash
poetry run pytest mvg_api/tests/api_tests.py
```

# Credit
For Endpoint Information and Code snippets
* https://github.com/leftshift/python_mvg_api
* https://www.mvg.de/
