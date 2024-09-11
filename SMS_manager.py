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
        if message.get("body").lower() == "hi truckle":
            if not check_person_database(message.get("number")):
                new_registrants_numbers.append(message.get("number"))
            else:
                print("this person has already registered")
                ##Use an update function here to update the status to: has to be sent the main menu 
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
        #whatever case that the person is in, they will be moving out of that state as this function only deals with new_messages received
        #So a message will be only evaluated in this section if the content of the message is replying to something that was sent out by the device/bot
    
        #No message sending happens here. Only the states get updated. 
        #If the input data from the message was correct then the cur state gets changed to "ready to send" or some number associated with that
        # The prev state then becomes what was the current state. E.g. 0, which is the state that says the welcome message was delivered.
        # Most states indicate a message being sent/waiting for a response. Only the "ready to send" state is for doing things
        # After updating the stats here, another function later goes through each person object and searches for any that have "ready to send"
        # By looking at the prev state, the function can figure out what is the next thing it has to send.
        #E.g. prev_state = 0. Message to send will be please enter your home address 

        #Also if at any time they send a "hi truckle" message everything will be reset and their state will go back to the main menu
        match person.current_state:
            case 0: #They have been sent the welcome message (request to enter name)
                #store name to database
                pass
            case 1: #They have been sent request to enter address - with an example hopefully
                #store address to database
                pass
            case 2: #Requested to confirm their registration details
                pass
            case 3: #Been sent a main menu. Options of book a pickup, share availability for a delivery, view existing pickup details, view existing delivery details, cancel existing delivery, cancel existing pickup, 
                pass
            ##Some more cases, if you could write it out tomorrow @Arthur

def send_message(phone_number:str, message_body:str):
    """
    Basically if you want to have a new line in your message body the string has to be written like:
    " "Hello World \n I am now on a new line" "
    The message body text that is passed to the termux-sms-send below has to have quotation marks around it for the new line function to work
    
    E.g.
    """
    message_body = f'"{message_body}"'
    subprocess.run(f"termux-sms-send -n {phone_number} {message_body}", shell=True)




def check_person_database(phone_number:str)->bool:
    #function to check if the given phon number already exists in the person database of both drivers and farmers.
    #Written this temporarily. Arthur, you would call the righ functions you've already written wherever this shows up.
    pass

def get_person_from_database(phone_number:str)->person_object:
    #searches the person database and then returns a object/dict of all the person's details 
    pass