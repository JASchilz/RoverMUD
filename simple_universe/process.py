#------------------------------------------------------------------------------
#   simple_universe/process.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

import interpreter as interpret


def process(character, this_input=False):
    """
    Process player commands and stimulation.
    """

    if not this_input:
        if character.brain.from_client:
            this_input = character.brain.from_client[0]
            character.brain.from_client = []

    if this_input.__class__.__name__ == "SimpleStim":
        if hasattr(character, 'brain') and hasattr(character.brain, 'client'):
            character.pc_process_stim(this_input)
        else:
            character.process_stim(this_input)

    elif this_input:
        [verb, rest] = interpret.verb(this_input)
        
        action_found = False

        for attachment in character.attachments:
            if action_found:
                break
            for action in attachment.action_matrix:
                if action[0] == verb:
                    action_found = True
                    action[1](rest)
                
        if not action_found:
            character.brain.to_client.append("I don't think you can actually do that...")
