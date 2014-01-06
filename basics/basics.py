#------------------------------------------------------------------------------
#   basics/basics.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#
#   These "base" objects are not used directly, but serve as parent classes
#   for the "things" and "characters" that occupy all "universes".
#
#------------------------------------------------------------------------------

import random
import weakref

class BaseThing():

    name = ""
    processor = False

    # All things occupy a container, such as a room or an inventory, and
    # some things may serve as containment for other things.
    container = False
    containment = False

    def process_stimuli(self, stimuli):
        """
        This function is called to handle stimuli directed at the "thing".
        """

        pass

    def move_to(self, container, containment):
        """
        Move a thing from one container to another.
        """

        # The thing's new container is container
        self.container = container

        # If the thing is presently in containment, remove it
        if self.containment:
            self.containment.remove(self)

        # Add the thing to its containment
        containment.append(self)
        self.containment = containment


class BaseCharacter(BaseThing):

    #password = ''
    #pass_salt = str(random.getrandbits(128))


    def __init__(self, client = False):
    
        if client:
            self.brain = PlayerBrain(self, client)
        
        self.attachments = []
        
    def disconnect(self):
    
        self.logged_in = False

class BaseAttachment():

    character = False
    action_matrix = False

    def __getstate__(self):
        result = self.__dict__.copy()
        del result['action_matrix']
        return result

    def __setstate__(self, thisDict):
        self.__init__(thisDict['character'])

        thisDict['action_matrix'] = self.action_matrix
        self.__dict__ = thisDict
        
        
class PlayerBrain(BaseAttachment):

    def __init__(self, character, client = False):

        self.password = ''
        self.pass_salt = str(random.getrandbits(128))
    
        self.client = client
        self.logged_in = False
        
        self.to_client = []
        self.from_client = []
    
        self.character = character

        self.action_matrix = []
        
        if client:
            self.client.brain = self
        
        self.prompt = ""
        
    def transplant(self, character):
    
        self.client.character = character
        self.character = character
        character.brain = self
        
        
    def cogitate(self):
        pass
        
        '''if self.to_client:
            self.character.to_client += self.to_client
            
        self.to_client = []'''

    
