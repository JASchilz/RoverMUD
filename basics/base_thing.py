from peewee import CharField, ForeignKeyField, Model, CompositeKey

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


class ContainerContainment(Model):
    """
    All things occupy a container, such as a room or an inventory, and
    some things may serve as containment for other things.
    """

    container = ForeignKeyField(BaseThing)
    containment = ForeignKeyField(BaseThing)

    class Meta:
        primary_key = CompositeKey('blog', 'tag')
