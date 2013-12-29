class SimpleWorld():

    zones = []

    def __init__(self, zones = False):

        self.zones = zones
        
        for zone in zones:
            for room in zone:
                room.set_world(self)
