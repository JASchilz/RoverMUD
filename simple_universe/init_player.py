from .character import SimpleCharacter, CHARACTER_LIST
from .the_world import DEFAULT_LOCATION, THIS_WORLD
from .simple_player_attachments import *


def init_player(character):
    """
    Initialize a player character into the simple_universe.
    """

    # Make the character a simple character, if they are not already.
    if not character.__class__.__name__ == "SimpleCharacter": # or True:
    
        old_character = character
        character = SimpleCharacter.from_simple_character(old_character)
        old_character.brain.transplant(character)
        
        # Give them the character attachments
        character.attachments.append(OOCComands(character))
        character.attachments.append((PlayerLegs(character)))
        character.attachments.append(PlayerEyes(character))
        character.attachments.append(PlayerMouth(character))
        character.attachments.append(PlayerArms(character))
        
        # Put them in the default location for players
        character.container = THIS_WORLD.zones[DEFAULT_LOCATION[0]][DEFAULT_LOCATION[1]]
        
        character.processor = process
        
    character.brain.prompt = "\n> "

    # Put them into the character list.
    CHARACTER_LIST.append(character)

    # Move the character into their room (refactor).
    character.move_to(character.room(), character.room().contents)
    process(character, "look")

    # Emit a visual stimulation to the room, excluding the character.
    this_message = character.name + " has entered the room."
    SimpleStim(STIM_VISUAL, this_message, False, [character.room()], [character])

    # Return the new character.
    return character
