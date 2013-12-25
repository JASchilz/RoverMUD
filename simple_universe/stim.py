STIM_VISUAL = 1
STIM_AUDIO = 2
STIM_DAMAGE = 3

class SimpleStim():

    stim_type = False
    stim_string = False
    stim_content = False

    targets = []
    target_exceptions = []

    def __init__(self, stim_type, stim_string, stim_content, targets,
                 target_exceptions=[], hold=False):

        self.stim_type = stim_type
        self.stim_string = stim_string
        self.stim_content = stim_content
        self.targets = targets
        self.target_exceptions = target_exceptions

        if not hold:
            self.emit()

    def emit(self):

        # Build the list of exceptions
        theseExceptions = []
        for exception in self.target_exceptions:
            if exception.__class__.__name__ == "SimpleRoom":
                for content in exception.contents:
                    theseExceptions.append(content)
            elif exception.__class__.__name__ == "SimpleWorld":
                for room in target.rooms:
                    for content in room.contents:
                        theseExceptions.append(content)
            else:
                theseExceptions.append(exception)

        for target in self.targets:
            if target.__class__.__name__ == "SimpleRoom":
                for content in target.contents:
                    if not content in theseExceptions:
                        process(content, self)

            elif target.__class__.__name__ == "list": #sloppy
                for room in target:
                    for content in room.contents:
                        if not content in theseExceptions:
                            process(content, self)
##            elif target.__class__.__name__ == "SimpleWorld"
##                for room in target.rooms:
##                    for content in room.contents:
##                        if not content in theseExceptions:
##                            process(content, self)

            else:
                # If we get here, it's because someone specifically listed
                # a character as a target. We don't check if they're in the
                # exceptions.
                process(target, self)
