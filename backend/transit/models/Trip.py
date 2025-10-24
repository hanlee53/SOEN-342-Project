import itertools
from typing import TYPE_CHECKING

# Use type checking block to avoid circular imports

from .Client import Client
from .Ticket import Ticket

class Trip:
   

    def __init__(self, tickets: list[Ticket], id:str):
        self.ticket_id = id
        self.tickets: Ticket = tickets

    def __str__(self):
        return f"Ticket #{self.ticket_id} for {self.client.name}"

