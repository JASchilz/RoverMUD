#------------------------------------------------------------------------------
#   simple_universe/room.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

class SimpleRoom():

    ID = [-1, -1]
    exits = []
    description = ""

    def __init__(self, ID = [-1, -1], exits = False, description = False,
                 contents = False):

        self.ID = ID
        self.exits = exits
        self.description = description
        
        self.THIS_WORLD = False

        self.contents = []
        if contents:
            for content in contents:
                content.move_to(self, self.contents)

    def resolve_exit(self, the_exit):

        if type(the_exit[1]) == type([]):
            return self.THIS_WORLD.zones[the_exit[1][0]][the_exit[1][1]]

        else:
            return self.THIS_WORLD.zones[self.ID[0]][the_exit[1]]

    def zone(self):

        return self.THIS_WORLD.zones[self.ID[0]]
        
    def set_world(self, world):
    
        self.THIS_WORLD = world
