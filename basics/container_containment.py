from peewee import CharField, ForeignKeyField, CompositeKey, IntegerField

from db.db import BaseModel


class ContainerContainment(BaseModel):
    """
    All things occupy a container, such as a room or an inventory, and
    some things may serve as containment for other things.
    """

    container = IntegerField()
    containment = IntegerField()

    container_class = CharField(max_length=255)
    containment_class = CharField(max_length=255)

    class Meta:
        primary_key = CompositeKey(
            'container', 'containment', 'container_class', 'containment_class'
        )