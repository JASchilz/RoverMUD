from basics import BaseAttachment

class OOCComands(BaseAttachment):

    character = False

    def __init__(self, character):
        self.character = character

        self.action_matrix = [
            ["help", self.do_help,
                "Open the help screen, or receive help on a specific command. \
                \n\tExamples: 'help', 'help quit'"],
            ["quit", self.do_quit, "Quit the game."],
            ["health", self.do_health, "Assess your health.\n\tAliases: 'h'."]
            ]

    def do_help(self, rest):
        output = "Help Information\n\nCOMMAND\tDESCRIPTION"
        for attachment in self.character.attachments:
            output += "\n"
            for action in attachment.action_matrix:
                output += action[0] + "\t" + action[2] + "\n"

        self.character.brain.to_client.append(output)

    def do_quit(self, rest):
        self.character.brain.client.active = False

    def do_health(self, rest):
        self.character.brain.to_client.append("You have " + str(self.character.current_hp) + " hit points.")
