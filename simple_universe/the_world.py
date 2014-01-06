#------------------------------------------------------------------------------
#   simple_universe/the_world.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

from thing import SimpleThing
from character import SimpleCharacter
from room import SimpleRoom
from world import SimpleWorld

from world_basics import zone_0

DEFAULT_LOCATION = [1, 0]


this_clock = SimpleThing("a bronze clock",
                "This is a large bronze clock, topped with a statue of an angel.",
                ["clock"])
this_stag = SimpleCharacter("a muscular stag", "This is a large brown stag.", 5,
                ["stag"], False)


zone_1 = []
zone_1.append(SimpleRoom([1, 0], [["north", 1], ["west", 2]],"You are in a somewhat plain bedroom. A door to the north opens into a library, and french doors to the west open onto a balcony.", [this_clock]))
zone_1.append(SimpleRoom([1, 1], [["south", 0], ["east", 3]], "Books line the walls from ceiling to floor. Exits lead south into a bedroom and east into the upper level of a foyer."))
zone_1.append(SimpleRoom([1, 2], [["east", 0]], "You're perched on a balcony here, 50 feet above wave tossed cliffs. Seagulls wheel overhead, and an island-speckled sea stretches out to the west. To the east, a door leads into a plain bedroom."))
zone_1.append(SimpleRoom([1, 3], [["east", 4], ["west", 1], ["down", 5]], "A narrow balcony wraps around this open room. Doors open to the east and west into a library and drawing room, while a staircase leads down to a foyer."))
zone_1.append(SimpleRoom([1, 4], [["west", 3]], "A red velvet couch overlooks south facing windows, in this dimly lit drawing room. A door to the east open onto the upper level of a foyer."))
zone_1.append(SimpleRoom([1, 5], [["up", 3], ["north", [2, 0]]], "Through french doors opening to the north, you see an exit into a pleasant forest scene. Inside, a staircase leads up towards a narrow balcony that opens onto several rooms."))

zone_2 = []
zone_2.append(SimpleRoom([2, 0], [["south", [1, 5]], ["west", 4], ["east", 5], ["north", 2]], "You're standing at the edge of a wooded glen. To the south, french doors open into a two-story house. The woods stretch out in all other directions."))

zone_2.append(SimpleRoom([2, 1], [["south", 4], ["east", 2]], "Cliffs of mossy rock bar your movement to the north and west, but the woods you're in extend in all other directions."))
zone_2.append(SimpleRoom([2, 2], [["south", 0], ["east", 3], ["west", 1]], "Cliffs of mossy rock bar your movement to the north, but the woods you're in extend in all other directions."))
zone_2.append(SimpleRoom([2, 3], [["south", 5], ["west", 2]], "Cliffs of mossy rock bar your movement to the north and east, but the woods you're in extend in all other directions."))
zone_2.append(SimpleRoom([2, 4], [["north", 1], ["east", 0]], "The face of a rocky cliff abruptly ends in a precipitous fall to the ocean, blocking movement west and south respectively. But the woods you're in extend in all other directions.", [this_stag]))
zone_2.append(SimpleRoom([2, 5], [["north", 3], ["west", 0]], "The face of a rocky cliff abruptly ends in a precipitous fall to the ocean, blocking movement eest and south respectively. But the woods you're in extend in all other directions."))

zones = [zone_0, zone_1, zone_2]


THIS_WORLD = SimpleWorld(zones)
