from basics import BaseAttachment


class PlayerMouth(BaseAttachment):

    character = False

    def __init__(self, character):
        self.character = character

        self.action_matrix = [
            ["say", self.do_say, "Say a message. Examples: 'say Hello.'. Alias: single quote mark"],
            ["shout", self.do_shout, "Shout out, or shout a message. Examples: 'shout', 'shout Hey!'"]
            ]

    def do_say(self, rest):

        if rest:
            self.character.brain.to_client.append("You say, '" + rest + "'")
            this_message = self.character.name + " says, '" + rest + "'"
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room()], [self.character])
        else:
            # improve with gender
            self.character.brain.to_client.append("You make a face as though you'd like to say something.")
            this_message = self.character.name + " makes a face as though they want to say something."
            SimpleStim(STIM_VISUAL, this_message, False, [self.character.room()], [self.character])

    def do_shout(self, rest):
        if rest:
            self.character.brain.to_client.append("You shout out, '" + rest + "'")

            this_message = "From a distance, you hear " + self.character.name + " shout, '" + rest + "'"
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room().zone()], [self.character.room()])

            this_message = self.character.name + " shouts, '" + rest + "'"
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room()], [self.character])

        else:

            if random() < .7: # just being a bit funny here
                self.character.brain.to_client.append("You shout in frustration.")
            else:
                self.character.brain.to_client.append("You shout in anger.")

            this_message = "You hear someone shout out in frustration, or possibly anger."
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room().zone()], [self.character.room()])

            this_message = self.character.name + " shouts out in frustration, or possibly anger."
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room()], [self.character])