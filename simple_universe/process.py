#------------------------------------------------------------------------------
#   simple_universe/process.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

import interpreter as interpret

def process(character, thisInput = False):
    '''
    Process player commands and stimulation.
    '''

    if not thisInput:
        if character.brain.from_client:
            thisInput = character.brain.from_client[0]
            character.brain.from_client = []

    if thisInput.__class__.__name__ == "SimpleStim":
        if hasattr(character, 'brain') and hasattr(character.brain, 'client'):
            character.pc_process_stim(thisInput)
        else:
            character.process_stim(thisInput)
            

    elif thisInput:
        [verb, rest] = interpret.verb(thisInput)
        
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
