from thing import SimpleThing

class SimpleRoom():

    ID = [-1, -1]
    exits = []
    description = ""

    def __init__(self, ID = [-1, -1], exits = False, description = False,
                 contents = False):

        self.ID = ID
        self.exits = exits
        self.description = description

        self.contents = []
        if contents:
            for content in contents:
                content.move_to(self, self.contents)

    def resolve_exit(self, the_exit):

        if type(the_exit[1]) == type([]):
            return THIS_WORLD.zones[the_exit[1][0]][the_exit[1][1]]

        else:
            return THIS_WORLD.zones[self.ID[0]][the_exit[1]]

    def zone(self):

        return THIS_WORLD.zones[self.ID[0]]


class SimpleWorld():

    zones = []

    def __init__(self, zones = False):

        self.zones = zones


A_CORPSE = SimpleThing("the corpse of ", "This is the corpse of ",
                ["corpse"], False)

this_clock = SimpleThing("a bronze clock",
                "This is a large bronze clock, topped with a statue of an angel.",
                ["clock"])
this_stag = SimpleMob("a muscular stag", "This is a large brown stag.",
                ["stag"], False)


zone_0 = []
zone_0.append(SimpleRoom([0, 0], [],
                "You have been destroyed. Prepare yourself for reclamation."))
zone_0.append(SimpleRoom([0, 1], [],
                "You are in limbo. With luck, you should soon be reincarnated \
                into the world."))

THE_TRASH = zone_0[0]
LIMBO = zone_0[1]


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


THIS_WORLD = SimpleWorld([zone_0, zone_1, zone_2])
