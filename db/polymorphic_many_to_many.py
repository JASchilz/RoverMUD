from peewee import CharField, CompositeKey, IntegerField

from db.db import BaseModel


class PolymorphicManyToMany(BaseModel):
    """
    All things occupy a container, such as a room or an inventory, and
    some things may serve as containment for other things.
    """

    a_id = IntegerField()
    b_id = IntegerField()

    a_class = CharField(max_length=255)
    b_class = CharField(max_length=255)

    class Meta:
        primary_key = CompositeKey(
            'a_id', 'b_id', 'a_class', 'b_class'
        )