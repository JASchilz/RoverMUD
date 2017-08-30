from basics import BaseAttachment
from simple_universe.simple_stim import SimpleStim, STIM_VISUAL
from simple_universe.process import process


class PlayerLegs(BaseAttachment):

    character = False

    def __init__(self, character):
        self.character = character

        self.action_matrix = [
            ["go", self.do_go,
                "Move in the specified direction.\n\tExample: 'go north', \
                'go up'. Aliases: 'north', 'n', 'south', etc."]
            ]

    def do_go(self, rest):

        if not rest:
            self.character.brain.to_client.append("OK, but go where?")

        elif rest in ["north", "south", "east", "west", "up", "down"]:

            exit_found = False

            for an_exit in self.character.room().exits:
                if rest == an_exit[0]:
                    exit_found = True

                    this_message = self.character.name + " leaves to the " + rest + "."
                    SimpleStim(STIM_VISUAL, this_message, False,
                                   [self.character.room()], [self.character])

                    new_room = self.character.room().resolve_exit(an_exit)

                    self.character.move_to(new_room, new_room.contents)
                    process(self.character, "look")

                    # Improve this, if you care to, with a direction of entry.
                    this_message = (self.character.name + " has entered the room.")
                    SimpleStim(STIM_VISUAL, this_message, False,
                               [self.character.room()], [self.character])

                    break

            if not exit_found:
                self.character.brain.to_client.append("You can't got that way from here.")

        else:
            self.character.brain.to_client.append("I don't understand that location or direction.")

