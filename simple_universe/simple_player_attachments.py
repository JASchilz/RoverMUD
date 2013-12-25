from basics import BaseAttachment
#from simple_stim import SimpleStim, STIM_VISUAL, STIM_AUDIO, STIM_VISUAL

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
            self.character.to_client.append("OK, but go where?")

        elif rest in ["north", "south", "east", "west", "up", "down"]:

            exit_found = False
            
            for an_exit in self.character.room().exits:
                if rest == an_exit[0]:
                    exit_found = True

                    this_message = self.character.name + " leaves to the " + \
                        rest + "."
                    SimpleStim(STIM_VISUAL, this_message, False,
                                   [self.character.room()], [self.character])

                    new_room = self.character.room().resolve_exit(an_exit)

                    self.character.move_to(new_room, new_room.contents)
                    process(self.character, "look")

                    # Improve this, if you care to, with a direction of entry.
                    this_message = (self.character.name +
                                   " has entered the room.")
                    SimpleStim(STIM_VISUAL, this_message, False,
                                   [self.character.room()], [self.character])
                    
                    break

            if not exit_found:
                self.character.to_client.append(
                    "You can't got that way from here.")

        else:
            self.character.to_client.append(
                "I don't understand that location or direction.")

class OOC_Commands(BaseAttachment):

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
                
        self.character.to_client.append(output)

    def do_quit(self, rest):
        self.character.client().active = False

    def do_health(self, rest):
        self.character.to_client.append("You have " +
                        str(self.character.current_hp) + " hit points.")

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
            self.character.to_client.append("OK, but take what?")
        else:
            thisParse = parse.parse(True, rest)

            theObject = find(self.character, thisParse)

            if theObject:

                if theObject == self.character:
                    self.character.to_client.append("Let's not explore that \
                        little conundrum, eh?")
                elif theObject.takable == True:
                    theObject.move_to(self.character, self.character.inventory)
                    self.character.to_client.append("You take " +
                                    theObject.short_description + ".")
                    
                    this_message = (self.character.name + " picks up " +
                                    theObject.short_description + ".")
                    SimpleStim(STIM_VISUAL, this_message, False,
                                   [self.character.room()], [self.character])
                    
                elif theObject.takable == False:
                    self.character.to_client.append("You're unable to take \
                        that.")
            else:
                self.character.to_client.append("I can't find the thing you'd \
                        like to take.")

    def do_drop(self, rest):

        if not rest:
            self.character.to_client.append("OK, but take what?")
        else:
            thisParse = parse.parse(True, rest)

            theObject = find(self.character, thisParse, self.character.inventory)

            if theObject:
                theObject.move_to(self.character.room(), self.character.room().contents)
                self.character.to_client.append("You drop " + theObject.short_description + ".")
                
                this_message = self.character.name + " sets down " + theObject.short_description + "."
                SimpleStim(STIM_VISUAL, this_message, False, [self.character.room()], [self.character])
            else:
                self.character.to_client.append("I can't find the thing you'd like to drop.")
                

    def do_hit(self, rest):

        if not rest:
            self.character.to_client.append("OK, but take what?")
        else:
            thisParse = parse.parse(True, rest)

            theObject = find(self.character, thisParse, self.character.room().contents)

            if theObject:
                if theObject.__class__.__name__ == "SimpleCharacter" or theObject.__class__.__name__ == "SimpleMob":
                    theObject.move_to(self.character.room(), self.character.room().contents)
                    self.character.to_client.append("You hit " + theObject.short_description + ".")

                    this_message = self.character.name + " smacks " + theObject.short_description + "."
                    SimpleStim(STIM_VISUAL, this_message, False, [self.character.room()], [self.character, theObject])

                    this_message = self.character.name + " hits you."
                    SimpleStim(STIM_DAMAGE, this_message, 1, [theObject], [])
                else:
                    self.character.to_client.append("You hit " + theObject.short_description + ".")
                    this_message = self.character.name + " smacks " + theObject.short_description + "."
                    SimpleStim(STIM_VISUAL, this_message, False, [self.character.room()], [self.character])
            else:
                self.character.to_client.append("I can't find the thing you'd like to hit.")
        

class PlayerEyes(BaseAttachment):

    character = False

    def __init__(self, character):
        self.character = character

        self.action_matrix = [
            ["look", self.do_look, "Look at your surroundings, or look at something.\n\tExamples: 'look', 'look at dog', 'look dog'. Aliases: 'l'"],
            ["inv", self.do_inventory, "View your inventory. Aliases: 'i'"]
            ]

    def do_look(self, rest):

        if rest == "":
            self.character.to_client.append(self.character.room().description)
            contents_description = "You see here: "
            for content in self.character.room().contents:
                if not content == self.character:
                    contents_description += content.short_description + ", "

            if not len(contents_description) == 14:
                contents_description = contents_description[0:len(contents_description) - 2] + "."
                self.character.to_client.append(contents_description)

            exits_description = "Exits lead: "
            for an_exit in self.character.room().exits:
                exits_description += an_exit[0] + ", "

            if len(exits_description) == 12:
                exits_description = "You see no exits."
                # Could do this a little nicer.

            else:
                exits_description = exits_description[0:len(exits_description) - 2] + "."
                
            self.character.to_client.append(exits_description)
        else:
            thisParse = parse.parse(True, rest)

            theObject = find(self.character, thisParse)

            if theObject:
                self.character.to_client.append(theObject.short_description)


            else:
                self.character.to_client.append("I can't find the thing you'd \
                        like to look at.")

            

    def do_inventory(self, rest):

        if rest == "":
            contents_description = "Your inventory contains: "
            for content in self.character.inventory:
                contents_description += content.short_description + ", "

            if not len(contents_description) == 25:
                contents_description = contents_description[0:len(contents_description) - 2] + "."
                self.character.to_client.append(contents_description)

            else:
                self.character.to_client.append("Your inventory is empty.")




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
            self.character.to_client.append("You say, '" + rest + "'")
            this_message = self.character.name + " says, '" + rest + "'"
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room()], [self.character])
        else:
            # improve with gender
            self.character.to_client.append("You make a face as though you'd like to say something.")
            this_message = self.character.name + " makes a face as though they want to say something."
            SimpleStim(STIM_VISUAL, this_message, False, [self.character.room()], [self.character])

    def do_shout(self, rest):
        if rest:
            self.character.to_client.append("You shout out, '" + rest + "'")
            
            this_message = "From a distance, you hear " + self.character.name + " shout, '" + rest + "'"
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room().zone()], [self.character.room()])

            this_message = self.character.name + " shouts, '" + rest + "'"
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room()], [self.character])
            
        else:
            
            if random() < .7: # just being a bit funny here
                self.character.to_client.append("You shout in frustration.")
            else:
                self.character.to_client.append("You shout in anger.")
                
            this_message = "You hear someone shout out in frustration, or possibly anger."
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room().zone()], [self.character.room()])

            this_message = self.character.name + " shouts out in frustration, or possibly anger."
            SimpleStim(STIM_AUDIO, this_message, False, [self.character.room()], [self.character])