import random

from peewee import CharField, DateTimeField

from .base_attachment import BaseAttachment


class PlayerBrain(BaseAttachment):

    username = CharField(max_length=255)
    password = CharField(max_length=255)

    pass_salt = CharField(max_length=255, default=lambda: str(random.getrandbits(128)))

    last_seen = DateTimeField()

    def __init__(self, character, client=False):

        super().__init__()

        self.client = client
        self.logged_in = False

        self.to_client = []
        self.from_client = []

        self.character = character

        self.action_matrix = []

        if client:
            self.client.brain = self

        self.prompt = ""

    def transplant(self, character):

        self.client.character = character
        self.character = character
        character.brain = self

    def cogitate(self):
        pass
