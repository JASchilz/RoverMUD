from basics import BaseAttachment

class PlayerEyes(BaseAttachment):

    character = False

    def __init__(self, character):
        self.character = character

        self.action_matrix = [
            ["look", self.do_look, "Look at your surroundings, or look at something.\n\tExamples: 'look', "
                                   "'look at dog', 'look dog'. Aliases: 'l'"],
            ["inv", self.do_inventory, "View your inventory. Aliases: 'i'"]
            ]

    def do_look(self, rest):

        if rest == "":
            self.character.brain.to_client.append(self.character.room().description)
            contents_description = "You see here: "
            for content in self.character.room().contents:
                if not content == self.character:
                    contents_description += content.short_description + ", "

            if not len(contents_description) == 14:
                contents_description = contents_description[0:len(contents_description) - 2] + "."
                self.character.brain.to_client.append(contents_description)

            exits_description = "Exits lead: "
            for an_exit in self.character.room().exits:
                exits_description += an_exit[0] + ", "

            if len(exits_description) == 12:
                exits_description = "You see no exits."
                # Could do this a little nicer.

            else:
                exits_description = exits_description[0:len(exits_description) - 2] + "."

            self.character.brain.to_client.append(exits_description)
        else:
            this_parse = interpret(True, rest)

            the_object = self.character.find(this_parse)

            if the_object:
                self.character.brain.to_client.append(the_object.short_description)

            else:
                self.character.brain.to_client.append("I can't find the thing you'd \
                        like to look at.")

    def do_inventory(self, rest):

        if rest == "":
            contents_description = "Your inventory contains: "
            for content in self.character.inventory:
                contents_description += content.short_description + ", "

            if not len(contents_description) == 25:
                contents_description = contents_description[0:len(contents_description) - 2] + "."
                self.character.brain.to_client.append(contents_description)

            else:
                self.character.brain.to_client.append("Your inventory is empty.")

