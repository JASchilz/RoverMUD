#------------------------------------------------------------------------------
#   simple_universe/world_basics.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

from .simple_thing import SimpleThing
from .room import SimpleRoom


zone_0 = []
zone_0.append(SimpleRoom([0, 0], [],
                "You have been destroyed. Prepare yourself for reclamation."))
zone_0.append(SimpleRoom([0, 1], [],
                "You are in limbo. With luck, you should soon be reincarnated \
                into the world."))
                

THE_TRASH = zone_0[0]
LIMBO = zone_0[1]


A_CORPSE = SimpleThing("the corpse of ", "This is the corpse of ",
                       ["corpse"], False)
