import interpreter as interpret

def process(character, thisInput = False):

    if not thisInput:
        if character.from_client:
            thisInput = character.from_client[0]
            character.from_client = []

    if thisInput.__class__.__name__ == "SimpleStim":
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
            character.to_client.append("I don't think you can actually do that...")
