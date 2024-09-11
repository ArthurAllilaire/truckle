####
####
"""
Just creating a seperate file for now. The functions below are how we will be reading messages from the device and some basic parsing included as well.
"""
####
####
import subprocess
import json
import datetime

#Function that runs the command below in shell and logs the output. It is a list of json dicts with the following attributes:
# {
#   threadid:int (the same for each phone number)
#   type:str (inbox, sent, draft, outbox)
#   read:bool (if the message has been read or not. This doesn't change unless you manually open the message with your fingers)
#   sender:str (a string of the persons)
#   number:str (phone number)
#   recieved:str (date+time. Although string, it looks like it is a datetime object converted to a string so it should be easy to change it back)
#   body:str (body of the message)
#   _id:int (each message, sent and received, gets an id) 
# }
def list_messages_inbox(limit:int = 15)-> list[dict]:
    msg_list_raw = subprocess.run(f"termux-sms-list -l {limit} -t inbox &", capture_output=True,text=True).stdout
    msg_list = json.loads(msg_list_raw)
    return msg_list

##Function used to filter out numbers that are registering for the first time
#It returns a list of phone numbers, stored as strings.
def filter_new_registrants(msg_list:list[dict])->list[str]:
    new_registrants_numbers = []
    for message in msg_list:
        if message.get("body").lower() == "activate truckle":
            if not check_person_database(message.get("number")):
                new_registrants_numbers.append(message.get("number"))
            else:
                print("this person has already registered")
                ##Use an update function here to update the status to: has to be sent "you've already registered"
    return new_registrants_numbers


#Function used to identify if there are any updated conversation messages from people.
#It does this by having an additional attribute stored with each person -> time of last sent message. Where sent means sent by the Truckle device to the public.
#If the received attribute on the message has a date that is more recent than the time of last sent message, then that get stored and sent for processing
def filter_existing_registrants(msg_list:list[dict])->list[str]:
    messages_to_be_processed = []
    for message in msg_list:
        if check_person_database(message.get("number")):
            person = get_person_from_database()
            if person.last_sent_message > datetime.strptime(message.get("recieved"),"%Y-%m-%d %H:%M:%S"):
                messages_to_be_processed.append(message)
            else:
                pass
        else:
            pass

    #This is checking for duplicates. In case people send two messages instead of just 1.
    #Will just reply back to them saying error and that have to resend the message as a single message.
    #messages_to_be_processed_2 has the revised list of messages to be processed. This list does not have duplicates caused by people sending two messages consequtively
    messages_to_be_processed_2 = []
    for message in messages_to_be_processed:
        number = message.get("number")
        if number in messages_to_be_processed_2:
            person = get_person_from_database(number)
            ##Update the state of the person to show error and that they should try and resend the info in a single message
        else:
            messages_to_be_processed_2.append(messages_to_be_processed_2)
    return messages_to_be_processed_2


def process_messages(message_to_be_processed:list[dict]):
    for message in message_to_be_processed:
        person = get_person_from_database(message.get("number"))
        match person.current_state:
            0 #They have been sent the welcome message
            1 #They have been sent request to 
            




def check_person_database(phone_number:str)->bool:
    #function to check if the given phon number already exists in the person database of both drivers and farmers.
    #Written this temporarily. Arthur, you would call the righ functions you've already written wherever this shows up.
    pass

def get_person_from_database(phone_number:str)->person_object:
    #searches the person database and then returns a object/dict of all the person's details 
    pass