#------------------------------------------------------------------------------
#   login_universe/universe.py
#   Copyright 2011-2013 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

import os
import pickle
import hashlib

from basics import BaseCharacter, BaseAttachment
from log import log

import simple_universe


# CHARACTER_LIST is the persistant list of characters which can
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
    '''
    A character in the login universe.
    '''

    # On initialization, we are awaiting the client's response
    # to the game's name query.
    login_state = AWAITING_NAME_QUERY

    def __init__(self, base_character = False):
    
        self.attachments = []
        self.brain = PlayerBrain(self)

        if base_character:
            self.to_client = base_character.to_client
            self.from_client = base_character.from_client

            self.client = base_character.client
            self.processor = base_character.processor

            self.logged_in = base_character.logged_in
            self.pass_salt = base_character.pass_salt
            
            
class PlayerBrain(BaseAttachment):

    character = False

    def __init__(self, character):
        self.character = character
        
        self.to_client = []
        self.action_matrix = []
        
    def cogitate(self):
        
        if self.to_client:
            self.character.to_client += self.to_client
            
        self.to_client = []
            


def process(character):
    '''
    Process the input and output of the LoginCharacter.
    '''

    if character.login_state == AWAITING_NAME_QUERY:
        character.to_client.append("Please enter your character name: ")
        character.login_state = AWAITING_NAME
        
    elif character.login_state == AWAITING_NAME:
        if character.from_client:

            character.supposed_character_name = clean_name(character.from_client[0])

            character.from_client = []
            if character.supposed_character_name == 'New':
                character.to_client.append("Creating a new character...")
                character.to_client.append("Please enter the name of your new character: ")
                character.login_state = AWAITING_NEW_CHARACTER_NAME
            else:
                character.login_state = AWAITING_PASSWORD
                character.to_client.append("Password: ")
                character.client().password_mode_on()
            
    elif character.login_state == AWAITING_PASSWORD:
        if character.from_client:
            character.supposed_password = character.from_client[0]
            character.from_client = []
            character.login_state = AWAITING_VALIDATION
            character.client().password_mode_off()
            character.to_client.append("\nValidating...")

    elif character.login_state == AWAITING_VALIDATION:
        result = is_character_of_name(character.supposed_character_name)

        if result:
            supposed_hash = hashlib.md5( result.pass_salt + character.supposed_password ).hexdigest()

        if result and supposed_hash == result.password:
            
            if result.logged_in:
                character.to_client.append("Character already logged in to game.")
                character.to_client.append("Allow some time for your old connection to time out, and try again.")
                character.login_state = AWAITING_NAME_QUERY
            else:

                CHARACTER_LIST.remove(result)
                
                character.client().character = result
                result.client = character.client
                
                result.logged_in = True
                result.to_client.append("User name and password validated.")
                result.to_client.append("Joining game...")

                result = simple_universe.init_character(result)

                CHARACTER_LIST.append(result)
        else:
            character.supposed_character_name = ''
            character.supposed_password = ''
            character.to_client.append("User name or password incorrect.")
            character.to_client.append("Please try again.")
            character.login_state = AWAITING_NAME_QUERY


    elif character.login_state == AWAITING_NEW_CHARACTER_NAME:
        if character.from_client:
            character.new_character_name = clean_name(character.from_client[0])
            character.from_client = []
            
            result = is_character_of_name(character.new_character_name)

            if not result:
                character.login_state = AWAITING_NEW_CHARACTER_NAME_CONF
                character.to_client.append('Confirm new character name "%s" (yes\\no): ' % character.new_character_name)
            else:
                character.to_client.append("This character name is already taken.")
                character.to_client.append("Please enter a different name for your new character: ")

    elif character.login_state == AWAITING_NEW_CHARACTER_NAME_CONF:
        if character.from_client:
            response = character.from_client[0].lower()
            if response[0] == 'y':
                character.to_client.append("You have accepted this name.")
                character.to_client.append("Enter a password for this character: ")
                character.client().password_mode_on()
                character.login_state = AWAITING_NEW_PASSWORD

            elif response[0] == 'n':
                character.to_client.append("You have declined this name.")
                character.to_client.append("Please enter the name of your new character: ")
                character.login_state = AWAITING_NEW_CHARACTER_NAME

            else:
                character.to_client.append("Response unrecognized.")
                character.to_client.append('Confirm or decline new character name "%s" by typing yes or no: ' % character.new_character_name)
                character.login_state = AWAITING_NEW_CHARACTER_NAME_CONF
                
            character.from_client = []

    elif character.login_state == AWAITING_NEW_PASSWORD:
        if character.from_client:
            character.new_password = character.from_client[0]
            character.from_client = []
            character.to_client.append("Reenter password to confirm: ")
            character.login_state = AWAITING_NEW_PASSWORD_CONF

    elif character.login_state == AWAITING_NEW_PASSWORD_CONF:
        if character.from_client:
            response = character.from_client[0]
            if response == character.new_password:
                character.to_client.append("Password confirmed.")
                character.client().password_mode_off()
                character.to_client.append("Please choose your character's sex (M\\F): ")
                character.login_state = AWAITING_SEX_SELECTION

            else:
                character.to_client.append("The two passwords you entered did not match.")
                character.to_client.append("Let's try again...")
                character.to_client.append("Enter a password for this character: ")
                character.login_state = AWAITING_NEW_PASSWORD
                
            character.from_client = []

    elif character.login_state == AWAITING_SEX_SELECTION:
        if character.from_client:
            response = character.from_client[0].lower()
            if response[0] == 'm':
                character.to_client.append("You have chosen to create a male character.")
                character.login_state = AWAITING_NEW_CHARACTER_FINALIZATION

            elif response[0] == 'f':
                character.to_client.append("You have chosen to create a female character.")
                character.login_state = AWAITING_NEW_CHARACTER_FINALIZATION

            else:
                character.to_client.append("Response unrecognized.")
                character.to_client.append('Please choose a sex for your character by typing either male or female: ')
                character.login_state = AWAITING_SEX_SELECTION
                
            character.from_client = []

    elif character.login_state == AWAITING_NEW_CHARACTER_FINALIZATION:
        character.name = character.new_character_name
        character.password = hashlib.md5( character.pass_salt + character.new_password ).hexdigest()
        character.logged_in = True

        character.to_client.append("Character created.")
        character.to_client.append("Joining game...")
        
        character = simple_universe.init_character(character)

        CHARACTER_LIST.append(character)

        backup_data()


def clean_name(name):
    '''
    Cleans a proposed character name.
    '''

    new_name = ''.join(ch for ch in name if ch.isalpha())
    new_name = new_name.title()

    return new_name

def is_character_of_name(name):
    '''
    Checks whether there is a character of the given name.
    '''

    for character in CHARACTER_LIST:
        if character.name == name:
            return character

    return False

                        
def init_character(character):
    '''
    Initialize characters into the login_universe.
    '''

    # Present the title screen
    try:
        title_screen = open(title_screen_file_path, 'r')
    except IOError:
        title_screen = open(title_screen_default_file_path, 'r')
        
        log("No custom title screen; using default.")

    title_text = ''

    for line in title_screen:
        title_text = title_text + line
        
    character.to_client.append(title_text)

    # Make the character a LoginCharacter
    character.client().character = LoginCharacter(character)
    character.client().character.processor = process
    
    # Clear the character's input queue
    character.client().character.from_client = [];

def backup_data():
    '''
    Backs up all player characters to file, logged in or not.
    '''
    
    # We have to momentarily remove everyone's client ref in order to
    # pickle the character file.
    clientDict = {}

    for character in CHARACTER_LIST:
        clientDict[character] = character.client
        character.client = False

    pickle.dump(CHARACTER_LIST, open(character_file_abs_file_path, "wb" ) )

    # And then we restore the clients to their characters
    for character in clientDict:
        character.client = clientDict[character]


def restore_data():
    '''
    Restores data on server boot
    '''

    global CHARACTER_LIST

    try:
        CHARACTER_LIST = pickle.load(open(character_file_abs_file_path, "rb" ))
    except IOError as e:
        print 'Error retrieving CHARACTER_LIST'

    for character in CHARACTER_LIST:
        character.logged_in = False
        character.to_client = []

def char_list():

    return CHARACTER_LIST


        
