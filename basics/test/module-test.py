from unittest import TestCase

from basics import BaseCharacter
from basics import BaseAttachment


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
        self.fail("Test unwritten")
