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

        self.container = container

        if self.containment:
            self.containment.remove(self)

        containment.append(self)
        self.containment = containment


class BaseCharacter(BaseThing):

    name = ''
    password = ''
    pass_salt = str(random.getrandbits(128))

    prompt = ''

    client = False

    logged_in = False
    
    to_client = []
    from_client = []

    def __init__(self, client = False):

        self.client = weakref.ref(client)
        
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

    
