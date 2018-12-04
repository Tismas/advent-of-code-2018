import re
import time
from datetime import datetime


def make_event(raw_data):
    date, message = [x.strip() for x in re.split(r'[\[|\]]', raw_data) if x]
    date = datetime.strptime(date, '%Y-%m-%d %H:%M')
    event = {'date': date, 'type': None, 'id': None}
    if message == 'wakes up' or message == 'falls asleep':
        event['type'] = message
    else:
        guard_id = message.split(' ')[1]
        event['type'] = 'begins shift'
        event['id'] = guard_id.split('#')[1]

    return event


with open('./input.txt') as f:
    guards = {}
    current_guard = None
    events = [make_event(x) for x in f.readlines()]
    events.sort(key=lambda x: x['date'])

    for event in events:
        if event['type'] == 'begins shift':
            current_guard = event['id']
            guards[current_guard] = guards.get(
                current_guard, {'time_slept': 0, 'sleep_history': []})
        elif event['type'] == 'falls asleep':
            guards[current_guard]['sleeping_since'] = event['date']
        else:
            guard = guards[current_guard]
            guard['time_slept'] += (
                event['date'] - guard['sleeping_since']).total_seconds() // 60
            guard['sleep_history'].append(
                {'start': guard['sleeping_since'], 'end': event['date']})
            guard['sleeping_since'] = None

    biggest_sleeper = max(guards.items(), key=lambda x: x[1]['time_slept'])
    sleeper_id = biggest_sleeper[0]
    sleeper_data = biggest_sleeper[1]

    minutes = {}
    for sleep_interval in sleeper_data['sleep_history']:
        for minute in range(sleep_interval['start'].minute, sleep_interval['end'].minute):
            minutes[minute] = minutes.get(minute, 0) + 1

    common_minute = max(minutes.items(), key=lambda x: x[1])[0]

    print('Strategy1 ID', sleeper_id)
    print('Strategy1 Common minute', common_minute)
    print('Strategy1 Multiplied', int(sleeper_id) * common_minute)

    minutes = {}
    for guard_id in guards:
        guard = guards[guard_id]
        minutes[guard_id] = {}
        for sleep_interval in guard['sleep_history']:
            for minute in range(sleep_interval['start'].minute, sleep_interval['end'].minute):
                minutes[guard_id][minute] = minutes[guard_id].get(minute, 0) + 1

    organized_sleeper_id = None
    repeated_minute = None
    repetition_record = 0
    for guard_id in minutes:
        for minute in minutes[guard_id]:
            repetitions = minutes[guard_id][minute]
            if repetitions > repetition_record:
                repetition_record = repetitions
                repeated_minute = minute
                organized_sleeper_id = guard_id

    print('Strategy2 ID', organized_sleeper_id)
    print('Strategy2 Common minute', repeated_minute)
    print('Strategy2 Repetitions', repetition_record)
    print('Strategy2 Multiplied', int(organized_sleeper_id) * repeated_minute)
