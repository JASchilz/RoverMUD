from unittest import TestCase

from basics import BaseCharacter
from basics import BaseAttachment
from basics import BaseThing


class ModuleTest(TestCase):

    def test_character_attach_attachment(self):
        character = BaseCharacter().save()
        attachment = BaseAttachment().save()

        # Attachment should not be among the character's attachments
        self.assertNotIn(attachment.id, character.attachments())

        # Attach the attachment
        character.attach(attachment)

        # Attachment should be among the character's attachments
        self.assertIn(attachment.id, character.attachments())

    def test_container_containment(self):
        thing_a = BaseThing().save()
        thing_b = BaseThing().save()

        # thing_b should not be among thing_a's stuff
        self.assertNotIn(thing_b.id, thing_a.stuff())

        # thing_b aint contained
        self.assertIsNone(thing_b.container())

        # Move thing_b into thing_a
        thing_b.move_to(thing_a)

        # thing_b should be among thing_a's stuff
        self.assertIn(thing_b.id, thing_a.stuff())

        # thing_b is contained by thing_a
        self.assertEqual(thing_a, thing_b.container())

