from .base_thing import BaseThing
from .player_brain import PlayerBrain
from .character_attachment import CharacterAttachment


class BaseCharacter(BaseThing):

    def __init__(self, client=False):

        if client:
            self.brain = PlayerBrain(self, client)

    def attach(self, attachment):
        CharacterAttachment.insert(
            container=self.primary_key,
            containment=attachment.primary_key,
            container_class=self.table,
            containment_class=attachment.table,
        )

    def disconnect(self):

        self.logged_in = False
