#------------------------------------------------------------------------------
#   simple_universe/character.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------
from random import random, randint, choice
import copy

from scheduler import schedule_event

from stim import SimpleStim, STIM_VISUAL, STIM_AUDIO, STIM_VISUAL
from simple_player_attachments import *
from the_world import SimpleRoom, SimpleWorld
from world_basics import LIMBO
from thing import SimpleThing
from basics import BaseCharacter
from mob import SimpleMob
from process import process
from the_world import DEFAULT_LOCATION, THIS_WORLD
from world_basics import LIMBO

# Here, CHARACTER_LIST is the transient list of characters that
# are actually in the universe.
CHARACTER_LIST = []


class SimpleCharacter(SimpleMob, BaseCharacter):

    where_goes_when_dies = LIMBO

    def __init__(self, base_character):

        self.container = THIS_WORLD.zones[DEFAULT_LOCATION[0]][DEFAULT_LOCATION[1]]

        self.attachments = []
        self.inventory = []

        self.to_client = base_character.to_client
        self.from_client = base_character.from_client

        self.client = base_character.client
        self.processor = process
        self.disconnector = disconnect

        self.logged_in = base_character.logged_in

        self.name = base_character.name
        self.password = base_character.password
        self.pass_salt = base_character.pass_salt
        self.prompt = "\n> "

        self.attachments.append(OOC_Commands(self))
        self.attachments.append((PlayerLegs(self)))
        self.attachments.append(PlayerEyes(self))
        self.attachments.append(PlayerMouth(self))
        self.attachments.append(PlayerArms(self))

        self.short_description = self.name
        self.keywords = [self.name.lower()]

    def process_stim(self, stim):

        if stim.stim_type == STIM_DAMAGE:
            self.current_hp -= stim.stim_content
            self.to_client.append(stim.stim_string + " You lose " +
                                  str(stim.stim_content) + " hit point.")

            if self.current_hp <= 0 and self.alive:
                self.to_client.append("That killed you.")
                self.alive = False
                # Figure out some more stuff to do here later.
        else:
            self.to_client.append(stim.stim_string)
            
    def find(self, subParse, theList = False):
            
        if subParse:

            if not theList:
                theList = self.room().contents

            for content in theList:
                for keyword in content.keywords:
                    if keyword == subParse[0]:
                        return content

        return False


    def __getstate__(self):
        result = self.__dict__.copy()
        result['container'] = result['container'].ID
        return result

    def __setstate__(self, thisDict):

        # This is sloppy, and supposes match up of ID to position, etc.
        thisDict['container'] = THIS_WORLD.zones[thisDict['container'][0]][thisDict['container'][1]]
        thisDict['containment'] = False
        self.__dict__ = thisDict





def disconnect(character):

    global CHARACTER_LIST

    character.logged_in = False
    character.room().contents.remove(character)

    CHARACTER_LIST.remove(character)

                        
def init_character(character):

    if not character.__class__.__name__ == "SimpleCharacter": #or True:

        character.client().character = SimpleCharacter(character)
        character.client().character.from_client = [];

    character = character.client().character

    CHARACTER_LIST.append(character)
    
    character.move_to(character.room(), character.room().contents)
    process(character, "look")

    this_message = character.name + " has entered the room."
    SimpleStim(STIM_VISUAL, this_message, False, [character.room()], [character])

    return character
