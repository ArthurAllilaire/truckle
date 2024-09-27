from typing import TypeAlias, Callable
from database import *
from vals import WELCOME_MESSAGE, OPTION_MESSAGE
import os
import re
import datetime
from delivery import Delivery, Driver, Farmer, Pickup
from person import Person, Activity

process_text = Callable[[tuple[Person, str]], str]

def dispatch_person(person: Person, message: str) -> str:
    """
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
    activity = person.activity
    activities: process_text = [
        start_activity,
        process_delivery,
        cancel_upcoming,
        see_upcoming,
        process_pickup,
        process_reg
    ]

    if activity is None:
        person.activity, person.status = 5, 0 #always register first
        return WELCOME_MESSAGE
    
    return activities[activity](person, message)

def dispatch_text(phone_num: int, message: str) -> str:
    # Gets details from database or creates person in database
    return dispatch_person(Person(phone_num), message)
    
    

def start_activity(person: Person, message: str) -> str:
    # print(int(message) in Activity) TODO - BETTER WAY THAN BELOW?
    if message.isdigit() and int(message) in range(len(Activity)):
        person.activity, person.status = int(message), 0 # starting activity
        return dispatch_person(person, message)
    return OPTION_MESSAGE




def cancel_upcoming(phone_num: int, status: int, message: str):
    pass

def cancel_upcoming(phone_num: int, status: int, message: str):
    pass

def see_upcoming(phone_num: int, status: int, message: str):
    pass

def process_delivery(phone_num: int):
    pass

def process_reg(person: Person, message: str) -> str:
    """
    First time user flow

    Status meanings
    0 - Name input
    1 - Name confirmation

    """
    if message == "5":
        return "Please enter your new name:"
    CONFIRM_NAME = f"Hey {message}! Please confirm you have correctly entered your name. Text 1 to confirm, 2 to re-enter."
    match person.status:
        case 0:
            person.status += 1
            person.name = message
            return CONFIRM_NAME
        case 1:
            if message == "1":
                person.is_confirmed = True
                # Finished activity - go back to dispatch text to get main menu
                person.activity = 0
                return OPTION_MESSAGE
            elif message == "2":
                # Restart status to the top
                person.status = 0
                return "Please enter a new name:"
            else:
                return "Please enter 1 to confirm or 2 to cancel."
            



def process_pickup(person: Person, message: str):
    """
    Currently making a new pickup request

        Status meanings
    0 - Collect date required
    1 - Collect trip wanted
    2 - Collect weight needed
    3 - Get confirmation
    
    """
    match person.status:
        case 0:
            person.status += 1
            # Get date for trip
            return "What date do you need a pickup on? (Please input in DD/MM format)"
        
        case 1:   
            #Make sure date is correct
            pickup_date = Person.parse_date(message)
            if not pickup_date:
                if message == "1":
                    person.activity, person.state = 0, 0
                    return dispatch_person(person, message)
                return "Please enter a valid date in DD/MM format"
            
            deliveries = get_deliveries(pickup_date)
            if not deliveries:
                # TODO - Show other deliveries on nearby dates
                return f"Unfortunately, there are no deliveries available for the {pickup_date}, please enter another date or 1 to cancel."
            # Store delivery date
            update_delivery_date(phone_num, delivery_date)
            # Ask them to input driver num they want
            
            person.status += 1
            return f"Here are the possible deliveries: \n f{deliveries}, please reply with the number of the delivery driver you would like to book."
        
    if status == 2:
        # Check number they booked has a delivery on the day?
        get_driver_deliveries()




def set_up():
    createDatabase(DATABASE)
    

if __name__ == "__main__":
    import os
    # Initial data
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    set_up()
    print(dispatch_text(7752715719, "hello"))
    # print(dispatch_text(2, "hello"))
    print(dispatch_text(7752715719, "Athur"))
    # print(dispatch_text(2, "3"))
    # print(dispatch_text(7752715719, "1/2"))
    print(dispatch_text(7752715719, "2"))
    print(dispatch_text(7752715719, "Arthur"))
    print(dispatch_text(7752715719, "happy!"))
    print(dispatch_text(7752715719, "happy!"))
    print(dispatch_text(7752715719, "happy!"))
    print(dispatch_text(7752715719, "1"))
    print(dispatch_text(7752715719, "5"))
    print(dispatch_text(7752715719, "5"))
    print(dispatch_text(7752715719, "Arthur"))
    print(dispatch_text(7752715719, "1"))
