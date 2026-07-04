# test_final_state.py
import os
import csv
from datetime import datetime, timedelta

def test_chat_summary_exists():
    """Check that the output summary CSV exists."""
    out_file = '/home/user/chat_summary.csv'
    assert os.path.exists(out_file), f"Output file {out_file} was not created."
    assert os.path.isfile(out_file), f"{out_file} is not a file."

def test_chat_summary_content():
    """Recompute the expected metrics from the raw data and validate the output."""
    raw_file = '/home/user/raw_chat.csv'
    out_file = '/home/user/chat_summary.csv'

    assert os.path.exists(raw_file), f"Raw file {raw_file} is missing."

    # Read and parse raw data
    raw_data = []
    with open(raw_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = datetime.fromisoformat(row['timestamp'])
            msg_len = len(row['message'].strip())
            raw_data.append({
                'ts': ts,
                'room': row['chat_room'],
                'msg_len': msg_len
            })

    assert raw_data, "Raw data is empty."

    min_ts = min(r['ts'] for r in raw_data)
    max_ts = max(r['ts'] for r in raw_data)

    start_hour = min_ts.replace(minute=0, second=0, microsecond=0)
    end_hour = max_ts.replace(minute=0, second=0, microsecond=0)

    rooms = sorted(list(set(r['room'] for r in raw_data)))

    # Aggregate by hour and room
    hourly_sums = {}
    curr = start_hour
    while curr <= end_hour:
        hourly_sums[curr] = {room: 0 for room in rooms}
        curr += timedelta(hours=1)

    for r in raw_data:
        hour = r['ts'].replace(minute=0, second=0, microsecond=0)
        hourly_sums[hour][r['room']] += r['msg_len']

    # Rolling 3-hour sum
    expected_output = {}
    curr = start_hour
    while curr <= end_hour:
        expected_output[curr] = {}
        for room in rooms:
            total = 0
            for i in range(3):
                h = curr - timedelta(hours=i)
                if h in hourly_sums:
                    total += hourly_sums[h][room]
            expected_output[curr][room] = total
        curr += timedelta(hours=1)

    # Read output file and compare
    with open(out_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            assert False, f"Output file {out_file} is empty."

        expected_headers = ['timestamp'] + rooms
        assert headers == expected_headers, f"Headers mismatch. Expected {expected_headers}, got {headers}"

        out_rows = list(reader)

    assert len(out_rows) == len(expected_output), f"Expected {len(expected_output)} rows, got {len(out_rows)}"

    curr = start_hour
    for row in out_rows:
        ts_str = curr.strftime('%Y-%m-%d %H:%M:%S')
        assert row[0] == ts_str, f"Expected timestamp '{ts_str}', got '{row[0]}'"
        for i, room in enumerate(rooms):
            expected_val = float(expected_output[curr][room])
            try:
                actual_val = float(row[i+1])
            except ValueError:
                assert False, f"Non-numeric value '{row[i+1]}' found for room '{room}' at timestamp '{ts_str}'"

            assert actual_val == expected_val, (
                f"Value mismatch at {ts_str} for room '{room}'. "
                f"Expected {expected_val}, got {actual_val}."
            )
        curr += timedelta(hours=1)