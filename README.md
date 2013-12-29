RoverMUD
========

A modular, object oriented, python based MUD.

Notable Features
----------------

### Attachments
"Attachments" allow perception and action.

For example, the player has "player legs" attached to their character. The legs register their commands ("west", "east", "north", etc.,) with the character's interpreter.

Likewise, "player eyes" register their "look" command with the character's interpreter. When another character enters the room, this action emits a visual stimulation targetted to all objects in the room; any player or non-player character with attached eyes will have that stimulation interpretted for them.

This system of attachments was designed to accomodate non-player characters. A set of "non-player eyes" would deliver visual stimulation to the character in a more uninterpretted, code-like form, suitable for interpretation by artificial intelligence routines.

### Universe
A "universe" is an isolated gameplay state with its own mechanics. There is presently a "login" universe in which the player creates a character or logs in, and a "simple" universe which will be included in the development and release versions of this project. A character is created in the login universe when the player initiates a connection and then translated into a simple-universe character and placed in the "simple" universe when they complete login. In principle, there could be multiple, isolated play-universes or multiple, connected universes with methods to translate characters and events from one into the other.

Requires
========

* python 2.7+ (2.6+?)

Usage
=====

```
$ python mud_main.py
```
    
You may then telnet to the server on port 7777. Recommend running RoverMUD server within a 'screen' session.

Type 'help' after logging in to see available commands.

Status
======

What Works
----------

* Creating a character
* Logging in
* Moving around
* Taking and dropping objects
* Looking at things
* Hitting and killing things

What Will Work After Refactor Completed
---------------------------------------

* Some of the commands in the help menu.


Immediate To-Do
---------------

* More architectural refactor to be completed.
* Move away from pickle for storage.
* Comments.
* Headers.

Later To-Do
-----------

* Building the simple universe into a more functional MUD.


License
=======

Apache License v2

Copyright (c) 2013, Joseph Schilz, Joseph@Schilz.org

