#!/usr/bin/env python
#------------------------------------------------------------------------------
#   mud_main.py
#   Copyright 2012 Joseph Schilz
#   
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
#   Derived in part from miniboa chat_demo.py, Copyright 2009 Jim Storch.
#------------------------------------------------------------------------------

import textwrap
import traceback
from time import sleep
from datetime import datetime

from miniboa import TelnetServer

import simple_universe
import login_universe
from basics import BaseCharacter
from scheduler import schedule_event, do_tick


IDLE_TIMEOUT = 300
CLIENT_LIST = []
SERVER_RUN = True

TIME_FORMAT = '%Y%m%d:%H%M%S: '


def on_connect(client):
    """
    Sample on_connect function.
    Handles new connections.
    """
    log("++ Opened connection to %s" % client.addrport())

    client.character = BaseCharacter(client)
    CLIENT_LIST.append(client)
    login_universe.init_character(client.character)


def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    log("-- Lost connection to %s" % client.addrport())
    client.character.logged_in = False
    client.character.client = False
    client.character.disconnector(client.character)
    client.send("\nDisconnecting\n")
    CLIENT_LIST.remove(client)


def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    ## Who hasn't been typing?
    for client in CLIENT_LIST:
        if client.idle() > IDLE_TIMEOUT:
            log('-- Kicking idle lobby client from %s' % client.addrport())
            client.active = False


def process_clients():
    """
    Check each client, if they are active, send them to their processor.
    If they have input, record it.
    If they have messages waiting, send them.
    """
    for client in CLIENT_LIST:
        
        if client.active:
            client.character.processor(client.character)

            if client.cmd_ready:
                this_command = client.get_command()
                if len(this_command) > 0:
                    client.character.from_client.append(this_command)

            if client.character.to_client:
                for msg in client.character.to_client:
                    if len(msg) <= 75 or "\n" in msg:
                        client.send("\n" + msg)
                    else:
                        client.send("\n" + textwrap.fill(msg, 75))

                if len(client.character.prompt) > 0:
                    client.send(client.character.prompt)

                client.character.to_client = []


def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in CLIENT_LIST:
        client.send(msg)

def log(msg):

    if len(msg) > 0:
        msg = msg[0] + msg[1:len(msg)].replace("\n", "\n    ")

        with open("log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime(TIME_FORMAT) + msg + "\n")

        print msg





#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------

if __name__ == '__main__':

    ## Simple chat server to demonstrate connection handling via the
    ## async and telnet modules.

    ## Create a telnet server with a port, address,
    ## a function to call with new connections
    ## and one to call with lost connections.

    telnet_server = TelnetServer(
        port=7777,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout = .05
        )

    log(">> Listening for connections on port %d.  CTRL-C to break."
        % telnet_server.port)

    login_universe.restore_data()

    tickCount = 0
    subtickCount = 0

    ## Server Loop

    try:
        while SERVER_RUN:
            sleep(.05)
            telnet_server.poll()    ## Send, Recv, and look for new connections
            kick_idle()             ## Check for idle clients
            process_clients()       ## Check for client input

            subtickCount += 1

            if subtickCount == 20:
                subtickCount = 0
                tickCount += 1
                do_tick()

            if (tickCount == 60 or tickCount % 360 == 0) and subtickCount == 0 and len(CLIENT_LIST) > 0:
                        
                login_universe.backup_data()
                log(">> Backing up character data.")

    except:
        tb = traceback.format_exc()
        log(">> FATAL ERROR\n" + tb)

    log(">> Server shutdown.")
