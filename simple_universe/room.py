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
