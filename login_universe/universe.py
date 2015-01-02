#------------------------------------------------------------------------------
#   login_universe/universe.py
#   Copyright 2011-2013 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

import os
import pickle
import hashlib

from basics import BaseCharacter, BaseAttachment, PlayerBrain
from log import log

import simple_universe


# CHARACTER_LIST is the persistent list of characters which can
# log in to the MUD.
CHARACTER_LIST = []

# To create a custom title screen, place it in the text file indicated
# by title_screen_rel_path
title_screen_rel_path = "title_screen.txt"
title_screen_default_rel_path = "title_screen_default.txt"

character_file_rel_path = "character_list.p"

this_dir = os.path.dirname(__file__)

title_screen_file_path = os.path.join(this_dir, title_screen_rel_path)
title_screen_default_file_path = os.path.join(this_dir, title_screen_default_rel_path)

character_file_abs_file_path = os.path.join(this_dir, character_file_rel_path)

# Character login states.
AWAITING_NAME_QUERY = 0
AWAITING_NAME = 1
AWAITING_PASSWORD = 2
AWAITING_VALIDATION = 3
AWAITING_INJECTION = 4

# Character creation states.
AWAITING_NEW_CHARACTER_NAME = 10
AWAITING_NEW_CHARACTER_NAME_CONF = 11
AWAITING_NEW_PASSWORD = 12
AWAITING_NEW_PASSWORD_CONF = 13
AWAITING_SEX_SELECTION = 14
AWAITING_NEW_CHARACTER_FINALIZATION = 15


class LoginCharacter(BaseCharacter):
    """
    A character in the login universe.
    """

    # On initialization, we are awaiting the client's response
    # to the game's name query.
    login_state = AWAITING_NAME_QUERY

    def __init__(self, base_character=None):
        # super(LoginCharacter, self).__init__()
    
        self.attachments = []
        # self.brain = PlayerBrain(self)
        self.processor = process

        if base_character is not None:
            self.brain = base_character.brain
            self.brain.prompt = ""
            # self.processor = base_character.processor

            self.pass_salt = base_character.brain.pass_salt
            

def process(character):
    """
    Process the input and output of the LoginCharacter.
    """

    if character.login_state == AWAITING_NAME_QUERY:
        character.brain.to_client.append("Please enter your character name: ")
        character.login_state = AWAITING_NAME
        
    elif character.login_state == AWAITING_NAME:
        if character.brain.from_client:

            character.supposed_character_name = clean_name(character.brain.from_client[0])

            character.brain.from_client = []
            if character.supposed_character_name == 'New':
                character.brain.to_client.append("Creating a new character...")
                character.brain.to_client.append("Please enter the name of your new character: ")
                character.login_state = AWAITING_NEW_CHARACTER_NAME
            else:
                character.login_state = AWAITING_PASSWORD
                character.brain.to_client.append("Password: ")
                character.brain.client.password_mode_on()
            
    elif character.login_state == AWAITING_PASSWORD:
        if character.brain.from_client:
            character.supposed_password = character.brain.from_client[0]
            character.brain.from_client = []
            character.login_state = AWAITING_VALIDATION
            character.brain.client.password_mode_off()
            character.brain.to_client.append("\nValidating...")

    elif character.login_state == AWAITING_VALIDATION:
        result = is_character_of_name(character.supposed_character_name)

        if result:
            supposed_hash = hashlib.md5(result.brain.pass_salt + character.supposed_password ).hexdigest()

        if result and supposed_hash == result.brain.password:
            
            if result.logged_in:
                character.brain.to_client.append("Character already logged in to game.")
                character.brain.to_client.append("Allow some time for your old connection to time out, and try again.")
                character.login_state = AWAITING_NAME_QUERY
            else:
            
                character.brain.password = supposed_hash
                character.brain.pass_salt = result.brain.pass_salt

                CHARACTER_LIST.remove(result)
                
                result.logged_in = True
                
                character.brain.transplant(result)
                
                result.brain.to_client.append("User name and password validated.")
                result.brain.to_client.append("Joining game...")
                
                result = simple_universe.init_player(result)
                
                CHARACTER_LIST.append(result)
                
        else:
            character.supposed_character_name = ''
            character.supposed_password = ''
            character.brain.to_client.append("User name or password incorrect.")
            character.brain.to_client.append("Please try again.")
            character.login_state = AWAITING_NAME_QUERY

    elif character.login_state == AWAITING_NEW_CHARACTER_NAME:
        if character.brain.from_client:
            character.new_character_name = clean_name(character.brain.from_client[0])
            character.brain.from_client = []
            
            result = is_character_of_name(character.new_character_name)

            if not result:
                character.login_state = AWAITING_NEW_CHARACTER_NAME_CONF
                character.brain.to_client.append('Confirm new character name "%s" (yes\\no): ' % character.new_character_name)
            else:
                character.brain.to_client.append("This character name is already taken.")
                character.brain.to_client.append("Please enter a different name for your new character: ")

    elif character.login_state == AWAITING_NEW_CHARACTER_NAME_CONF:
        if character.brain.from_client:
            response = character.brain.from_client[0].lower()
            if response[0] == 'y':
                character.brain.to_client.append("You have accepted this name.")
                character.brain.to_client.append("Enter a password for this character: ")
                character.brain.client.password_mode_on()
                character.login_state = AWAITING_NEW_PASSWORD

            elif response[0] == 'n':
                character.brain.to_client.append("You have declined this name.")
                character.brain.to_client.append("Please enter the name of your new character: ")
                character.login_state = AWAITING_NEW_CHARACTER_NAME

            else:
                character.brain.to_client.append("Response unrecognized.")
                character.brain.to_client.append('Confirm or decline new character name "%s" by typing yes or no: ' % character.new_character_name)
                character.login_state = AWAITING_NEW_CHARACTER_NAME_CONF
                
            character.brain.from_client = []

    elif character.login_state == AWAITING_NEW_PASSWORD:
        if character.brain.from_client:
            character.new_password = character.brain.from_client[0]
            character.brain.from_client = []
            character.brain.to_client.append("Reenter password to confirm: ")
            character.login_state = AWAITING_NEW_PASSWORD_CONF

    elif character.login_state == AWAITING_NEW_PASSWORD_CONF:
        if character.brain.from_client:
            response = character.brain.from_client[0]
            if response == character.new_password:
                character.brain.to_client.append("Password confirmed.")
                character.brain.client.password_mode_off()
                character.brain.to_client.append("Please choose your character's sex (M\\F): ")
                character.login_state = AWAITING_SEX_SELECTION

            else:
                character.brain.to_client.append("The two passwords you entered did not match.")
                character.brain.to_client.append("Let's try again...")
                character.brain.to_client.append("Enter a password for this character: ")
                character.login_state = AWAITING_NEW_PASSWORD
                
            character.brain.from_client = []

    elif character.login_state == AWAITING_SEX_SELECTION:
        if character.brain.from_client:
            response = character.brain.from_client[0].lower()
            if response[0] == 'm':
                character.brain.to_client.append("You have chosen to create a male character.")
                character.login_state = AWAITING_NEW_CHARACTER_FINALIZATION

            elif response[0] == 'f':
                character.brain.to_client.append("You have chosen to create a female character.")
                character.login_state = AWAITING_NEW_CHARACTER_FINALIZATION

            else:
                character.brain.to_client.append("Response unrecognized.")
                character.brain.to_client.append('Please choose a sex for your character by typing either male or female: ')
                character.login_state = AWAITING_SEX_SELECTION
                
            character.brain.from_client = []

    elif character.login_state == AWAITING_NEW_CHARACTER_FINALIZATION:
        character.name = character.new_character_name
        character.brain.password = hashlib.md5( character.brain.pass_salt + character.new_password ).hexdigest()
        character.logged_in = True

        character.brain.to_client.append("Character created.")
        character.brain.to_client.append("Joining game...")
        
        character = simple_universe.init_player(character)

        CHARACTER_LIST.append(character)

        backup_data()


def clean_name(name):
    """
    Cleans a proposed character name.
    """

    new_name = ''.join(ch for ch in name if ch.isalpha())
    new_name = new_name.title()

    return new_name


def is_character_of_name(name):
    """
    Checks whether there is a character of the given name.
    """

    for character in CHARACTER_LIST:
        if character.name == name:
            return character

    return False

                        
def init_character(character):
    """
    Initialize characters into the login_universe.
    """

    # Present the title screen
    try:
        title_screen = open(title_screen_file_path, 'r')
    except IOError:
        title_screen = open(title_screen_default_file_path, 'r')
        
        log("No custom title screen; using default.")

    title_text = ''

    for line in title_screen:
        title_text += line
        
    character.brain.to_client.append(title_text)

    # Make the character a LoginCharacter
    character.brain.client.character = LoginCharacter(character)
    # character.client().brain.processor = process
    
    # Clear the character's input queue
    # character.client().character.brain.from_client = [];


def backup_data():
    """
    Backs up all player characters to file, logged in or not.
    """
    
    # We have to momentarily remove everyone's client in order to
    # pickle the character file.
    client_dict = {}

    for character in CHARACTER_LIST:
        client_dict[character] = character.brain.client
        character.brain.client = False

    pickle.dump(CHARACTER_LIST, open(character_file_abs_file_path, "wb"))

    # And then we restore the clients to their characters
    for character in client_dict:
        character.brain.client = client_dict[character]


def restore_data():
    """
    Restores data on server boot
    """

    global CHARACTER_LIST

    try:
        CHARACTER_LIST = pickle.load(open(character_file_abs_file_path, "rb"))
    except IOError as e:
        print 'Error retrieving CHARACTER_LIST'

    for character in CHARACTER_LIST:
        character.logged_in = False
        character.to_client = []


def char_list():

    return CHARACTER_LIST