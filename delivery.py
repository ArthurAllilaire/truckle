"""
File to manage deliveries (update, create and delete)
all stored in a class and accwessed through delivery objects which
track actual deliveries in the database.

Docs:
1. 

"""
from dataclasses import dataclass
from datetime import date
from typing import Any, Optional
from database import DATABASE, sqlite3
from person import Person, Activity

"""
Requirements:

Delivery(driver: Person)
delivery.weight, date, location

capacity needs to trigger calculation
date needs to trigger check for existing deliveries

Need to be able to get all upcoming deliveries

Pickups:
 all upcoming
 update weight, date, location, etc.
 cancel and update corresponding deliveries - text drivers abt changes - send text







is_confirmed - extra override as need to change database when setting - getting should not need database search
When fetching - which database do we use first?

Pickup

pickup.fetch_possible() -> return 
"""




# @dataclass
# class Delivery:
#     driver: Person
#     weight: int
#     date: date
#     location: str
#     capacity: int
#     is_confirmed: bool = False

class Delivery:
    ATTRS = ["weight", "date", "location"]
    def __init__(self, person: Person) -> None:
        self.person: Person = person
        self.con = sqlite3.connect(DATABASE)
        # First searches confirmed
        self._is_confirmed = True
        if not self.delivery_exists():
            self._is_confirmed = False # This switches self.table_name
            # Searches temp_
            if not self.delivery_exists():
                self.create_delivery() # defaults to temp_ table

    @property
    def table_name(self) -> str:
        name = ""
        if not self._is_confirmed:
            name = "temp_"
        return name + "delivery"

    
    @property
    def is_confirmed(self) -> bool:
        return self._is_confirmed

    def create_delivery(self, table_name = None) -> None:
        if not table_name:
            table_name = self.table_name
        with self.con:
            insert_query = f"""INSERT INTO {table_name} (driverNum, weight, date, location)
            VALUES (?, ?, ?, ?);
            """
            self.con.execute(insert_query, (self.person.phone_num, self.weight, self.date, self.location))

    def delete_delivery(self, table_name) -> None:
        with self.con:
            delete_query = f"""
                DELETE FROM {table_name}
                WHERE driverNum = ? AND date = ?
            """
            self.con.execute(delete_query, (self.person.phone_num, self.date))

    def get_vals(self):
        with self.con:
            query = f"""SELECT * FROM {self.table_name} WHERE driverNum = ? AND DATE = ?"""
            return self.con.execute(query, (self.person.phone_num, self.date)).fetchone()

    @is_confirmed.setter
    def is_confirmed(self, value: bool) -> None:
        """
        """
        #If set to same don't do anything
        if value == self._is_confirmed:
            return None
        if value:
            self.delete_delivery()
            # Get all values
            # Store temporarily
            # Delete the old delivery
            # Switch tables
            # Create new delivery

            self.create_delivery("delivery")
        else:
            self.add_delivery("temp_delivery")
            # Not always going to delete
            self.delete_delivery("delivery")

        self._is_confirmed = value
        

    def _query_attr(self, name: str):
        try:
            with self.con:
                res = self.con.execute(f'SELECT {name} FROM {self.table_name} WHERE phoneNum = {self.phone_num}').fetchone()
                if res:
                    # Unpack single value tuple
                    return res[0]
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return None

    def _set_query(self, name: str, val: Any) -> None:
        try:
            with self.con:
                update_query = f"""
                    UPDATE {self.table_name}
                    SET {name} = ?
                    WHERE phoneNum = ?
                """
                self.con.execute(update_query, (val, self.phone_num))
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return None
        
    def __getattribute__(self, name: str) -> Any:
        if name in Delivery.ATTRS:
            return self._query_attr(name)
        
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in Delivery.ATTRS:
            return self._set_query(name, value)
        
        return super().__setattr__(name, value)
    
    def delivery_exists(self) -> tuple[bool, bool]:
        """
        Returns (exists, is_confirmed) - is_confirmed false is exists false
        """
        with self.con:
            res = self.con.execute(f'SELECT * FROM {self.table_name} WHERE phoneNum = {self.phone_num}').fetchone()
            return res is not None
    
    def __del__(self):
        if self.con:
            self.con.close()