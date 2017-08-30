from basics import BaseAttachment

class PlayerArms(BaseAttachment):

    character = False

    def __init__(self, character):
        self.character = character

        self.action_matrix = [
            ["take", self.do_take, "Take an item from the world \
                into your inventory.\n\tExamples: 'take clock', 'take sword'"],
            ["drop", self.do_drop, "Drop an item from your inventory \
                into the world.\n\tExamples: 'drop clock"],
            ["hit", self.do_hit, "Hit something or someone in \
                violence.\n\tExamples: 'hit Dave'"]
            ]

    def do_take(self, rest):

        if not rest:
            self.character.brain.to_client.append("OK, but take what?")
        else:
            this_parse = interpret(True, rest)

            the_object = self.character.find(this_parse)

            if the_object:

                if the_object == self.character:
                    self.character.brain.to_client.append("Let's not explore that \
                        little conundrum, eh?")

                elif the_object.takable is True:
                    the_object.move_to(self.character, self.character.inventory)
                    self.character.brain.to_client.append("You take " +
                                    the_object.short_description + ".")

                    this_message = (self.character.name + " picks up " +
                                    the_object.short_description + ".")
                    SimpleStim(STIM_VISUAL, this_message, False,
                                   [self.character.room()], [self.character])

                elif the_object.takable is False:
                    self.character.brain.to_client.append("You're unable to take \
                        that.")
            else:
                self.character.brain.to_client.append("I can't find the thing you'd \
                        like to take.")

    def do_drop(self, rest):

        if not rest:
            self.character.brain.to_client.append("OK, but drop what?")
        else:
            this_parse = interpret(True, rest)

            the_object = self.character.find(this_parse, self.character.inventory)

            if the_object:
                the_object.move_to(self.character.room(), self.character.room().contents)
                self.character.brain.to_client.append("You drop " + the_object.short_description + ".")

                this_message = self.character.name + " sets down " + the_object.short_description + "."
                SimpleStim(STIM_VISUAL, this_message, False, [self.character.room()], [self.character])
            else:
                self.character.brain.to_client.append("I can't find the thing you'd like to drop.")

    def do_hit(self, rest):

        if not rest:
            self.character.brain.to_client.append("OK, but hit what?")
        else:
            this_parse = interpret(True, rest)

            the_object = self.character.find(this_parse, self.character.room().contents)

            if the_object:
                if the_object.__class__.__name__ == "SimpleCharacter" or the_object.__class__.__name__ == "SimpleMob":
                    the_object.move_to(self.character.room(), self.character.room().contents)
                    self.character.brain.to_client.append("You hit " + the_object.short_description + ".")

                    this_message = self.character.name + " smacks " + the_object.short_description + "."
                    SimpleStim(STIM_VISUAL, this_message, False, [self.character.room()], [self.character, the_object])

                    this_message = self.character.name + " hits you."
                    SimpleStim(STIM_DAMAGE, this_message, 1, [the_object], [])
                else:
                    self.character.brain.to_client.append("You hit " + the_object.short_description + ".")
                    this_message = self.character.name + " smacks " + the_object.short_description + "."
                    SimpleStim(STIM_VISUAL, this_message, False, [self.character.room()], [self.character])
            else:
                self.character.brain.to_client.append("I can't find the thing you'd like to hit.")

