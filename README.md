# expo-echo
Synchronize from Expobooking to echo.lu

This is an early state prototype showing how to query the Expobooking GraphQL API for planned events. It is planned to evolve the main application into a synchronization client that takes events from Expo and puts or updates them on echo.lu. It shall also contain basic client libraries for both APIs for those who don't want to bother with the GraphQL or the REST APIs directly.

## Installation

Create a virtualenv:

`$ python3 -m venv venv`

Activate it:

`$ . venv/bin/activate`

Install dev dependencies:

`$ python3 -m pip install pip-tools`

Install dependencies:

`$ pip-compile && pip-sync`

Copy configuration temlate:

`$ cp config.py.template config.py`

Fill in API key:

`$ edit config.py`

Run:

`$ python3 expo-echo.py`
