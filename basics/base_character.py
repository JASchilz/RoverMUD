from .base_thing import BaseThing
from .player_brain import PlayerBrain
from .character_attachment import CharacterAttachment


class BaseCharacter(BaseThing):

    def __init__(self, client=False):

        if client:
            self.brain = PlayerBrain(self, client)

