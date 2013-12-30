#------------------------------------------------------------------------------
#   simple_universe/thing.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

from basics import BaseThing

class SimpleThing(BaseThing):

    name = ""
    description = ""
    keywords = []

    takable = True

    def __init__(self, name, description, keywords=[], takable=True):

        self.name = name
        self.description = description
        self.keywords = keywords

        self.takable = takable

        self.short_description = self.name
        
    def process_stim(self, stim):
        pass

    def room(self):

        answer = self.container

        while not answer.__class__.__name__ == "SimpleRoom":
            answer = answer.container

        return answer
