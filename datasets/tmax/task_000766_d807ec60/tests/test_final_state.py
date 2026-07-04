# test_final_state.py

import os
import csv
import re

def test_summary_csv_exists_and_format():
    csv_path = '/home/user/summary.csv'
    assert os.path.exists(csv_path), f"File {csv_path} is missing."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['time', 'path', 'count'], f"CSV header is incorrect: {header}"

        rows = list(reader)
        assert len(rows) == 30, f"Expected 30 rows (10 minutes * 3 paths), got {len(rows)}"

        # Verify sorting
        for i in range(1, len(rows)):
            prev_time, prev_path = rows[i-1][0], rows[i-1][1]
            curr_time, curr_path = rows[i][0], rows[i][1]

            # Check chronological sort, then alphabetical by path
            if prev_time == curr_time:
                assert prev_path <= curr_path, f"Paths not sorted alphabetically for time {curr_time}: {prev_path} came before {curr_path}"
            else:
                assert prev_time < curr_time, f"Times not sorted chronologically: {prev_time} came before {curr_time}"

def test_summary_csv_data():
    csv_path = '/home/user/summary.csv'
    assert os.path.exists(csv_path), f"File {csv_path} is missing."

    data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    def get_count(time_str, path_keyword):
        matches = [int(row['count']) for row in data if row['time'] == time_str and path_keyword in row['path']]
        assert len(matches) == 1, f"Expected exactly 1 match for time {time_str} and path containing {path_keyword}, got {len(matches)}"
        return matches[0]

    # 10:00
    assert get_count('2023-10-24 10:00', 'users') == 1, "Count for users at 10:00 should be 1"
    assert get_count('2023-10-24 10:00', 'item') == 1, "Count for item at 10:00 should be 1"
    assert get_count('2023-10-24 10:00', 'status') == 0, "Count for status at 10:00 should be 0"

    # 10:02
    assert get_count('2023-10-24 10:02', 'users') == 1, "Count for users at 10:02 should be 1"
    assert get_count('2023-10-24 10:02', 'item') == 1, "Count for item at 10:02 should be 1"

    # 10:05
    assert get_count('2023-10-24 10:05', 'users') == 1, "Count for users at 10:05 should be 1"

    # 10:09
    assert get_count('2023-10-24 10:09', 'status') == 1, "Count for status at 10:09 should be 1"

def test_cron_schedule():
    cron_path = '/home/user/cron_schedule.txt'
    assert os.path.exists(cron_path), f"File {cron_path} is missing."

    with open(cron_path, 'r', encoding='utf-8') as f:
        cron = f.read().strip()

    assert cron.startswith('*/5 * * * *') or cron.startswith('0,5,10,15,20,25,30,35,40,45,50,55 * * * *'), \
        f"Cron schedule does not run every 5 minutes: {cron}"

    assert '/home/user/run_pipeline.sh' in cron, \
        f"Cron schedule does not contain the correct script path: {cron}"