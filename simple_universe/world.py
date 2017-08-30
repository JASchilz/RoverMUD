#------------------------------------------------------------------------------
#   simple_universe/world.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------


class SimpleWorld(object):

    zones = []

    def __init__(self, zones=False):

        self.zones = zones
        
        for zone in zones:
            for room in zone:
                room.set_world(self)
