from .base_thing import BaseThing
from .player_brain import PlayerBrain


class BaseCharacter(BaseThing):

    # password = ''
    # pass_salt = str(random.getrandbits(128))

    def __init__(self, client=False):

        if client:
            self.brain = PlayerBrain(self, client)

        self.attachments = []

    def disconnect(self):

        self.logged_in = False
