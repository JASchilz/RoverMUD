#------------------------------------------------------------------------------
#   login_universe/universe.py
#   Copyright 2011 Joseph Schilz
#   Figure out license
#------------------------------------------------------------------------------

from basics import BaseCharacter
from random import random, randint, choice
from scheduler import schedule_event

import parser as parse
import copy

from stim import SimpleStim, STIM_VISUAL, STIM_AUDIO, STIM_VISUAL
from simple_player_attachments import *
from thing import SimpleThing
from the_world import SimpleRoom, SimpleWorld, A_CORPSE, LIMBO, THE_TRASH



# Here, CHARACTER_LIST is the transient list of characters that
# are actually in the universe.
CHARACTER_LIST = []

DEFAULT_LOCATION = [1, 0]



class SimpleMob(SimpleThing):
    
    alive = True
    takable = False

    where_goes_when_dies = THE_TRASH

    def __init__(self, name, description, keywords=[], takable=False):

        self.name = name
        self.description = description
        self.keywords = keywords

        self.takable = takable

        self.short_description = self.name

        schedule_event(0, lambda: self.cogitate())

    def make_corpse(self):

        new_corpse = copy.copy(A_CORPSE)
        new_corpse.name += self.name
        new_corpse.description += self.name + "."
        new_corpse.short_description = new_corpse.name

        return new_corpse

    def die(mob):
    
        new_corpse = make_corpse(mob)
        new_corpse.move_to(mob.room(), mob.room().contents)
        
        self.move_to(self.where_goes_when_dies,
                    self.where_goes_when_dies.contents)

    def move_in_zone(self):

        exit_list = []
        
        for an_exit in self.room().exits:
            if type(an_exit[1]) == int or an_exit[1][0] == self.room().ID[0]:
                exit_list.append(an_exit)

        if exit_list:
            this_exit = choice(exit_list)
            this_destination = self.room().resolve_exit(this_exit)
            
            this_message = (
                self.name + " moves " + this_exit[0] + ".").capitalize()
            SimpleStim(STIM_VISUAL, this_message, False,
                [self.room()], [self])

            self.move_to(this_destination, this_destination.contents)

            this_message = (self.name + " enters.").capitalize()
            SimpleStim(STIM_VISUAL, this_message, False,
                [this_destination], [self])


    def process_stim(self, stim):

        if stim.stim_type == STIM_DAMAGE:
            self.current_hp -= stim.stim_content

            if self.current_hp <= 0 and self.alive:
                self.alive = False
                die(self)
                

    def cogitate(self):

        schedule_event(randint(10,30), lambda: self.move_in_zone())
        schedule_event(30, lambda: self.cogitate())

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


    def __getstate__(self):
        result = self.__dict__.copy()
        result['container'] = result['container'].ID
        return result

    def __setstate__(self, thisDict):

        # This is sloppy, and supposes match up of ID to position, etc.
        thisDict['container'] = THIS_WORLD.zones[thisDict['container'][0]][thisDict['container'][1]]
        thisDict['containment'] = False
        self.__dict__ = thisDict
    





def process(character, thisInput = False):

    if not thisInput:
        if character.from_client:
            thisInput = character.from_client[0]
            character.from_client = []

    if thisInput.__class__.__name__ == "SimpleStim":
        character.process_stim(thisInput)
            

    elif thisInput:
        [verb, rest] = parse.verb(thisInput)
        
        action_found = False

        for attachment in character.attachments:
            if action_found:
                break
            for action in attachment.action_matrix:
                if action[0] == verb:
                    action_found = True
                    action[1](rest)
                
        if not action_found:
            character.to_client.append("I don't think you can actually do that...")

def find(character, subParse, theList = False):
            
    if subParse:

        if not theList:
            theList = character.room().contents

        for content in theList:
            for keyword in content.keywords:
                if keyword == subParse[0]:
                    return content

    return False

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
