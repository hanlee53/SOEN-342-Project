# transit/models/__init__.py

# This file makes the 'models' folder a Python package
# and tells Django what models are available.

from .Connection import Connection
from .Station import Station
from .Client import Client
from .Ticket import Ticket
from .Trip import Trip

# This makes it so you can import them like
# from transit.models import Connection, Station, Trip
__all__ = [
    'Connection',
    'Station',
    'Ticket',
    'Client',
    'Trip'
]
