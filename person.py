from database import DATABASE, sqlite3
from enum import Enum
from typing import Optional, Any
import re
from datetime import date
class Activity(Enum):
    """
    Activity meaning:
    None - Hasn't contacted the number yet
    0 - No transactions in progress
    1 - Launch delivery (collect date)
    2 - launch cancel
    3 - launch upcoming
    4 - launch find delivery (triggered by DD/MM)
    5 - Edit Name
    """
    NO_ACTIVITY = 0
    NEW_DELIVERY = 1
    CANCEL_UPCOMING = 2
    SEE_UPCOMING = 3
    NEW_PICKUP = 4
    EDIT_NAME = 5


# Person in database: phone_num, name, activity, status, confirmed
# person_entry = list[int, str | None, int, int, bool]
class Person:
    ATTRS = ["name", "activity", "status", "is_confirmed"]
    def __init__(self, phone_num: int) -> None:
        self.phone_num: int = phone_num
        self.con = sqlite3.connect(DATABASE)
        if not self.person_exists():
            self._create_person()

    def _query_attr(self, name: str) -> Optional[str | int | bool]:
        with self.con:
            res = self.con.execute(f'SELECT {name} FROM people WHERE phoneNum = {self.phone_num}').fetchone()
            if res:
                # Unpack single value tuple
                return res[0]

    def _set_query(self, name: str, val: Any) -> None:
        try:
            with self.con:
                update_query = f"""
                    UPDATE people
                    SET {name} = ?
                    WHERE phoneNum = ?
                """
                self.con.execute(update_query, (val, self.phone_num))
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return None
        
    def __getattribute__(self, name: str) -> Any:
        if name in Person.ATTRS:
            return self._query_attr(name)
        
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in Person.ATTRS:
            return self._set_query(name, value)
        return super().__setattr__(name, value)
    
    def person_exists(self) -> bool:
        with self.con:
            res = self.con.execute(f'SELECT * FROM people WHERE phoneNum = {self.phone_num}').fetchone()
            return res is not None
    
    def __del__(self):
        if self.con:
            self.con.close()
    
    def _create_person(self) -> None:
        """
        Adds person so should only be called once!!
        This assumes person does not exist
        """
        with self.con:
            insert_query = """
                INSERT INTO people (phoneNum)
                VALUES (?);
                """
            self.con.execute(insert_query, (self.phone_num, ))
        
    # TODO - USE ENUM for self.activity instead of int
    
    def parse_date(message: str) -> Optional[date]:
        # Regular expression for matching DD/MM or D/M dates
        pattern = r"\b(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])\b"

        # Search for the first match
        match = re.search(pattern, message)

        # Check if a match is found and print it
        if match:
            return date(date.today().year, int(match.group(1)), int(match.group(2)))

