#------------------------------------------------------------------------------
#   log.py
#   Copyright 2013 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

from datetime import datetime

TIME_FORMAT = '%Y%m%d:%H%M%S: ' # Time format for the log.

def log(msg):
    """
    Make an entry into log.txt.
    """

    if len(msg) > 0:
        msg = msg[0] + msg[1:len(msg)].replace("\n", "\n    ")

        with open("log.txt", "a") as myfile:
            myfile.write(datetime.now().strftime(TIME_FORMAT) + msg + "\n")

        print msg
