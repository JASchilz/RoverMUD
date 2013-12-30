from random import randint, choice
from copy import copy

from scheduler import schedule_event

from thing import SimpleThing
from world_basics import THE_TRASH, A_CORPSE

from stim import SimpleStim, STIM_DAMAGE, STIM_VISUAL

class SimpleMob(SimpleThing):
    
    alive = True
    takable = False

    where_goes_when_dies = THE_TRASH

    def __init__(self, name, description, hp, keywords=[], takable=False):

        self.name = name
        self.description = description
        self.keywords = keywords
        
        self.current_hp = hp
        self.max_hp = hp

        self.takable = takable

        self.short_description = self.name

        schedule_event(0, lambda: self.cogitate())

    def make_corpse(self):

        new_corpse = copy(A_CORPSE)
        new_corpse.name += self.name
        new_corpse.description += self.name + "."
        new_corpse.short_description = new_corpse.name

        return new_corpse

    def die(self):
    
        new_corpse = self.make_corpse()
        new_corpse.move_to(self.room(), self.room().contents)
        
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
                self.die()
                

    def cogitate(self):

        schedule_event(randint(10,30), lambda: self.move_in_zone())
        schedule_event(30, lambda: self.cogitate())
