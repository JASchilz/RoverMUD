#------------------------------------------------------------------------------
#   basics/basics.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

import random
import weakref

class BaseThing():

    processor = False

    container = False
    containment = False

    def process_stimuli(self, stimuli):

        pass

    def move_to(self, container, containment):

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

    disconnector = False

    client = False

    logged_in = False
    
    to_client = []
    from_client = []

    def __init__(self, client = False):

        self.client = weakref.ref(client)

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

    
