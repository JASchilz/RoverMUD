from peewee import CharField

from db.db import BaseModel


class BaseThing(BaseModel):

    name = CharField(max_length=255)
    processor = False

    def process_stimuli(self, stimuli):
        """
        This function is called to handle stimuli directed at the "thing".
        """

        pass

    def move_to(self, container, containment):
        """
        Move a thing from one container to another.
        """

        # The thing's new container is container
        self.container = container

        # If the thing is presently in containment, remove it
        if self.containment:
            self.containment.remove(self)

        # Add the thing to its containment
        containment.append(self)
        self.containment = containment



