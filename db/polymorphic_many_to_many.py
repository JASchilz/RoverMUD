from peewee import CharField, CompositeKey, IntegerField

from db.db import BaseModel


class PolymorphicManyToMany(BaseModel):
    """
    All things occupy a container, such as a room or an inventory, and
    some things may serve as containment for other things.
    """

    a_id = IntegerField()
    b_id = IntegerField()

    a_table = CharField(max_length=255)
    b_table = CharField(max_length=255)

    class Meta:
        primary_key = CompositeKey(
            'a_id', 'b_id', 'a_table', 'b_table'
        )

    @staticmethod
    def associate(cls, a, b):
        cls.insert(
            a_id=a.primary_key,
            b_id=b.primary_key,
            a_table=a.table,
            b_table=b.table,
        )
        
    @staticmethod
    def dissociate(cls, a, b):
        cls.where(a_id=a.primary_key, b_id=b.primary_key, a_table=a.table, b_table=b.table).delete()

