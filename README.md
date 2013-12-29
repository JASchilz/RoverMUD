RoverMUD
========

A modular, object oriented, python based MUD.

Notable features presented colloquially:

```
A "universe" is an isolated gameplay state with its own mechanics. Right now there is a "login" universe in which the player creates a character or logs in, and a "simple" universe which is the room-based MUD I'm building. A character is created in the login universe when they initiate a connection and then translated into a simple-universe character and placed in the "simple" universe when they complete login. In principle, there could be multiple play-universes that could be isolated from each other, or have ways to translate characters and events from one into the other.

"player attachments" allow perception and action. So I create "player legs" and attach them to you as a player. The legs register their commands ("west", "east", "north", etc.,) with your interpreter. Likewise, I give you "player eyes" that register their "look" command with your interpreter, and also deliver "visual stimuli" from your surroundings to your terminal. Whereas "NPC eyes" would deliver visual stimuli to the NPC in a more basic, code-like form.
```

Requires
========

* python 2.7+ (2.6+?)

Usage
=====

```
$ python mud_main.py
```
    
You may then telnet to the server on port 7777. Recommend running RoverMUD within a 'screen' session.

Status
======

What Works
----------

* Creating a character
* Logging in

What Doesn't Work
-----------------

The following will work once I complete a refactor

* Moving around
* Looking at things
* Hitting and killing things
* Taking and dropping objects

Other Status Notes
------------------

More refactor to be completed.

License
=======

Apache License v2

Copyright (c) 2013, Joseph Schilz, Joseph@Schilz.org

