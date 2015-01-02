#------------------------------------------------------------------------------
#   scheduler/scheduler.py
#   Copyright 2011 Joseph Schilz
#   Licensed under Apache v2
#------------------------------------------------------------------------------

schedule = {}
time = 0


def schedule_event(delta_t, event):
    """
    Schedule an event delta_t ticks in the future.
    """

    global schedule

    schedule.setdefault(time + delta_t, []).append(event)


def do_tick():
    """
    Execute scheduled events.
    """

    global time
    time += 1

    for key in schedule.keys():
        if key <= time:
            events = schedule.pop(key)
            for event in events:
                event()
        else:
            break



