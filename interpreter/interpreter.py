#------------------------------------------------------------------------------
#   interpreter/interpreter.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

articles = [" a ", " the "]

def verb(command):
    # A function to isolate the verb in a command.

    thisVerb = ""
    theRest = ""

    firstSpace = command.find(" ")

    # If thisInput contains a space, the verb is everything before the
    # first space.
    if firstSpace > 0:
        thisVerb = command[0:firstSpace]
        theRest = command[firstSpace + 1:len(command)]
    # If it doesn't contain a space, the whole thing is the verb.
    else:
        thisVerb = command

    # We handle simple verb aliases at this level...
    if command[0] == "'":
        thisVerb = "say"
        theRest = command[1:len(command)]

    if command == "north" or command == "n":
        thisVerb = "go"
        theRest = "north"
    elif command == "south" or command == "s":
        thisVerb = "go"
        theRest = "south"
    elif command == "east" or command == "e":
        thisVerb = "go"
        theRest = "east"
    elif command == "west" or command == "w":
        thisVerb = "go"
        theRest = "west"
    elif command == "up" or command == "u":
        thisVerb = "go"
        theRest = "up"
    elif command == "down" or command == "d":
        thisVerb = "go"
        theRest = "down"

    if thisVerb == "l":
        thisVerb = "look"
    elif thisVerb == "i":
        thisVerb = "inv"
    elif thisVerb == "h":
        thisVerb = "health"


    return thisVerb, theRest

def interpret(theVerb, theRest, transitivity = 1):

    theRest = " " + theRest.lower() + " "

    for article in articles:
        theRest = theRest.replace(article, '')

    if transitivity == 1:
        theRest = theRest.strip().split()

        if len(theRest) > 0:
            # This might not be stable.
            return [theRest.pop(), theRest]

        else:
            return False
