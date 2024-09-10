from typing import TypeAlias, Callable
from drivers import *
from vals import WELCOME_MESSAGE
import os
import re
import datetime

process_text = Callable[[tuple[int, int, str]], str]

# Have to create database for beginning script
def dispatch_text(phone_num: int, message: str) -> str:
    """
    Activity meaning:
    None - Hasn't contacted the number yet
    0 - No transactions in progress
    1 - Launch delivery (collect date)
    2 - launch cancel
    3 - launch upcoming
    4 - launch find delivery (triggered by DD/MM)

    Status meaning for each activity:
    For 0 - No status
    For 1:
    0 - Collect date
    1 - Get weight for delivery
    2 - Get location for delivery
    3 - Get confirmation

    For 2:
    0 - Collect trip to cancel
    1 - Get confirmation

    For 3 - No status

    For 4:
    0 - Collect trip number
    1 - Collect weight needed
    2 - Get confirmation
    """
    activity, status = get_person(phone_num)
    activities: process_text = [
        start_activity,
        process_delivery,
        cancel_upcoming,
        see_upcoming,
        process_pickup
    ]

    if activity is None:
        set_activity(phone_num, 0)
        return WELCOME_MESSAGE
    
    return activities[activity](phone_num, status, message)
    

def start_activity(phone_num: int, status: int, message: str) -> str:
    if message.isdigit() and int(message) in range(1,5):
        update_activity(phone_num, int(message))
        update_status(phone_num, 0) # back to 0 as starting activity
        return dispatch_text(phone_num, message)
    return WELCOME_MESSAGE




def cancel_upcoming(phone_num: int, status: int, message: str):
    pass

def cancel_upcoming(phone_num: int, status: int, message: str):
    pass

def see_upcoming(phone_num: int, status: int, message: str):
    pass

def process_delivery(phone_num: int):
    pass

def process_pickup(phone_num: int, status: int, message: str):
    """
    Currently making a new pickup request or just looking at future pickups
    (NEED TO BE ABLE TO CANCEL)

    Status meanings
    0 - Collect date required
    1 - Collect trip wanted
    2 - Collect weight needed
    3 - Get confirmation
    
    """
    if status == 0:
        # Get date for trip
        update_status(phone_num, status + 1)
        return "What date do you need a pickup on? (Please input in DD/MM format)"
    
    if status == 1:
        #Make sure date is correct
        # Regular expression for matching DD/MM or D/M dates
        pattern = r"\b(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])\b"

        # Search for the first match
        match = re.search(pattern, message)

        # Check if a match is found and print it
        if match:
            update_status(phone_num, status + 1)
            delivery_date = date(date.today().year, int(match.group(1)), int(match.group(2)))
            deliveries = str(get_deliveries(delivery_date))
            #NEED TO STORE ORDERED LIST of deliveries till next step
            return f"Here are the possible deliveries: \n f{deliveries}, please reply with the number of your favourite delivery."
    
        return "Please enter a valid date in DD/MM format"    
    if status == 2:
        print("We got here!")




def set_up():
    createDatabase(DATABASE)
    

if __name__ == "__main__":
    import os
    # Initial data
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    set_up()
    print(dispatch_text(7752715719, "hello"))
    print(dispatch_text(2, "hello"))
    print(dispatch_text(7752715719, "4"))
    print(dispatch_text(2, "3"))
    print(dispatch_text(7752715719, "1/2"))
    print(dispatch_text(7752715719, "4"))