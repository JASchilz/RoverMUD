#------------------------------------------------------------------------------
#   log.py
#   Copyright 2013 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

import os
from datetime import datetime

TIME_FORMAT = '%Y%m%d:%H%M%S: '  # Time format for the log.


def log(msg):
    """
    Make an entry into log.txt.
    """

    if len(msg) > 0:
        msg = msg[0] + msg[1:len(msg)].replace("\n", "\n    ")

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")

        with open(path, "a") as my_file:
            my_file.write(datetime.now().strftime(TIME_FORMAT) + msg + "\n")

        print(msg)
