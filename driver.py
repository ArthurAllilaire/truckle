from dataclasses import dataclass
from datetime import date
from typing import Any, Optional
from database import DATABASE, sqlite3
from person import Person, Activity

@dataclass
class Pickup:
    driver: Person
    farmer: Person
    weight: int
    date: date
    is_confirmed: bool = False



class Driver():
    def __init__(self, person: Person) -> None:
        self.person = person

    def get_all_deliveries() -> list[Delivery]:
        pass

class Farmer():
    def __init__(self, person: Person) -> None:
        self.person = person

    def get_all_pickups() -> list[Pickup]:
        pass