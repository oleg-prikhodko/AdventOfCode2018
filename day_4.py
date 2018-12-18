import re
from collections import Counter, defaultdict, namedtuple
from datetime import datetime

from day_2 import load_strings

LogEntry = namedtuple("LogEntry", "time message")


def load_logs(lines):
    log_entries = []
    for line in lines:
        match = re.search(r"\[(.+)\] (.+)$", line)
        log_entries.append(
            LogEntry(datetime.fromisoformat(match.group(1)), match.group(2))
        )

    return sorted(log_entries, key=lambda log_entry: log_entry.time)


def divide_logs_by_guard(logs):
    logs_by_guard = defaultdict(list)
    last_guard_id = None
    for log in logs:
        match = re.search(r"#(\d+)", log.message)
        if match is not None:
            last_guard_id = int(match.group(1))
            continue
        logs_by_guard[last_guard_id].append(log)

    return logs_by_guard


def get_minutes_asleep(asleep_minute, awoke_minute):
    return list(range(asleep_minute, awoke_minute))


def get_sleep_duration(asleep_minute, awoke_minute):
    return awoke_minute - asleep_minute


if __name__ == "__main__":
    lines = load_strings("input_4.txt")
    logs = load_logs(lines)
    logs_by_guard = divide_logs_by_guard(logs)

    max_asleep_minute_by_guard = dict()
    total_sleep_duration_by_guard = defaultdict(int)

    for guard_id, logs in logs_by_guard.items():
        # print(guard_id, len(logs) % 2 == 0)
        minutes_asleep = []
        for asleep_log, awoke_log in zip(logs[::2], logs[1::2]):
            minutes_asleep.extend(
                get_minutes_asleep(
                    asleep_log.time.minute, awoke_log.time.minute
                )
            )
            total_sleep_duration_by_guard[guard_id] += get_sleep_duration(
                asleep_log.time.minute, awoke_log.time.minute
            )
        sleep_minutes = Counter(minutes_asleep)
        minute, reps = sleep_minutes.most_common(1)[0]
        max_asleep_minute_by_guard[guard_id] = minute, reps

    sleepiest_guard_id, _ = max(
        total_sleep_duration_by_guard.items(), key=lambda item: item[1]
    )
    sleepiest_minute, _ = max_asleep_minute_by_guard[sleepiest_guard_id]
    print(sleepiest_guard_id * sleepiest_minute)

    guard_who_sleeps_most_on_same_minute, minute_info = max(
        max_asleep_minute_by_guard.items(), key=lambda item: item[1][1]
    )
    print(guard_who_sleeps_most_on_same_minute * minute_info[0])
