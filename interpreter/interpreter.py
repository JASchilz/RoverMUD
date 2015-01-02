#------------------------------------------------------------------------------
#   interpreter/interpreter.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

articles = [" a ", " the "]


def verb(command):
    # A function to isolate the verb in a command.

    this_verb = ""
    the_rest = ""

    first_space = command.find(" ")

    # If this_input contains a space, the verb is everything before the
    # first space.
    if first_space > 0:
        this_verb = command[0:first_space]
        the_rest = command[first_space + 1:len(command)]
    # If it doesn't contain a space, the whole thing is the verb.
    else:
        this_verb = command

    # We handle simple verb aliases at this level...
    if command[0] == "'":
        this_verb = "say"
        the_rest = command[1:len(command)]

    if command == "north" or command == "n":
        this_verb = "go"
        the_rest = "north"
    elif command == "south" or command == "s":
        this_verb = "go"
        the_rest = "south"
    elif command == "east" or command == "e":
        this_verb = "go"
        the_rest = "east"
    elif command == "west" or command == "w":
        this_verb = "go"
        the_rest = "west"
    elif command == "up" or command == "u":
        this_verb = "go"
        the_rest = "up"
    elif command == "down" or command == "d":
        this_verb = "go"
        the_rest = "down"

    if this_verb == "l":
        this_verb = "look"
    elif this_verb == "i":
        this_verb = "inv"
    elif this_verb == "h":
        this_verb = "health"

    return this_verb, the_rest


def interpret(the_verb, the_rest, transitivity=1):

    the_rest = " " + the_rest.lower() + " "

    for article in articles:
        the_rest = the_rest.replace(article, '')

    if transitivity == 1:
        the_rest = the_rest.strip().split()

        if len(the_rest) > 0:
            # This might not be stable.
            return [the_rest.pop(), the_rest]

        else:
            return False
