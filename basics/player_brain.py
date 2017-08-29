import random

from .base_attachment import BaseAttachment


class PlayerBrain(BaseAttachment):

    def __init__(self, character, client=False):

        self.password = ''
        self.pass_salt = str(random.getrandbits(128))

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
