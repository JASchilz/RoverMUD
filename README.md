RoverMUD
========

A modular, object oriented, python based MUD.

Communications provided by Jim Storch's miniboa. No dependencies on external libraries.

Notable Features
----------------

### Attachments
"Attachments" allow perception and action.

For example, the player has "player legs" attached to their character. The legs register their commands ("west", "east", "north", etc.,) with the character's interpreter.

Likewise, "player eyes" register their "look" command with the character's interpreter. When another character enters the room, this action emits a visual stimulation targetted to all objects in the room; any player or non-player character with attached eyes will have that stimulation interpretted for them.

This system of attachments was designed to accomodate non-player characters. A set of "non-player eyes" would deliver visual stimulation to the character in a more uninterpretted, code-like form, suitable for interpretation by artificial intelligence routines.

### Universe
A "universe" is an isolated gameplay state with its own mechanics. There is presently a "login" universe in which the player creates a character or logs in, and a "simple" universe which will be included in the development and release versions of this project. A character is created in the login universe when the player initiates a connection and then translated into a simple-universe character and placed in the "simple" universe when they complete login. In principle, there could be multiple, isolated play-universes or multiple, connected universes with methods to translate characters and events from one into the other.

Goals
-----

This project will produce a well documented and architectured MUD that demonstrates the capability and methodology of the codebase. This project will not produce a fully-featured, production MUD. I would happily connect developers who are interested in working together on such a project, or help manage pull requests for such a project.

Requires
--------

* python 2.7 or 3.5
* miniboa

Install
-------

```

$> git clone https://github.com/JASchilz/RoverMUD.git
$> cd RoverMud
$> pip install -r requirements.txt

```

Usage
-----

```
$> python mud_main.py
```
    
You may then telnet to the server on port 7777. Recommend running RoverMUD server within a 'screen' session.

Type 'help' after logging in to see available commands.


Status
------

Though the basic functions of a MUD are functional, I would consider the code 'unstable' until the items in the 'immediate to-do' have been completed. Any fork made at this point will not be compatible architecturally with the first release version.

The code is currently messy following a merge of character and mob in simple_universe.

### What Works

* Scheduling
* Creating a character
* Logging in
* Moving around
* Taking and dropping objects
* Looking at things
* Hitting and killing things
* All commands in 'help'

### Notable To-Do's Done

* Merge character and mob

### Immediate To-Do

* Refactor persistance to [peewee](https://github.com/coleifer/peewee)
* Create an "admin" such that deployment is along the lines of `pip install rovermud; rovermud begin --midgaard; revermud serve`
* Use a logging library for logging
* Bring process and process_stim under brain
* Bring the attachment system, especially regarding perception, to spec
* Fix container/containment

### Later To-Do

* OLC
* Experience and leveling
* Wearing and wielding
* A larger world (eg: Midgaard) for the simple world.
* NPC AI examples


Contributing
------------

Anyone interested in helping the codebase move to an ORM may contact me. I believe it would be best to hold off on adding new features until that move has been completed.

With that in mind, feel free to open pull requests or issues. [GitHub](https://github.com/JASchilz/RoverMUD/) is the canonical location of this project. Here's the general sequence of events for code contribution:

1. Open an issue in the [issue tracker](https://github.com/JASchilz/RoverMUD/issues/).
2. In any order:
  * Submit a pull request with a **failing** test that demonstrates the issue/feature.
  * Get acknowledgement/concurrence.
3. Revise your pull request to pass the test in (2). Include documentation, if appropriate.


License
-------

Apache License v2

Copyright (c) 2013, Joseph Schilz, Joseph@Schilz.org

