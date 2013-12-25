schedule = {}
time = 0

def do_tick():

    global time
    time += 1

    for key in schedule.keys():
        if key <= time:
            events = schedule.pop(key)
            for event in events:
                event()
        else:
            break


def schedule_event(delta_t, event):

    global schedule

    schedule.setdefault(time + delta_t, []).append(event)
