# test_final_state.py

import os
import csv
import stat

def get_expected_output(input_file):
    events = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                events.append((int(row[0]), row[1], row[2]))

    if not events:
        return []

    first_ts = events[0][0]
    w_start = first_ts - (first_ts % 60)

    windows = {}
    last_window = w_start

    for ts, cat, desc in events:
        w = ts - (ts % 60)
        while last_window < w:
            if last_window not in windows:
                windows[last_window] = {}
            last_window += 60

        if w not in windows:
            windows[w] = {}

        if cat not in windows[w]:
            windows[w][cat] = desc

        last_window = w

    expected_lines = []
    for w in sorted(windows.keys()):
        for cat in ['DB', 'NET', 'SEC']:
            desc = windows[w].get(cat, 'NO_CHANGE')
            expected_lines.append(f"{w},{cat},{desc}")

    return expected_lines

def test_source_and_executable_exist():
    source_path = '/home/user/process_configs.c'
    exec_path = '/home/user/process_configs'

    assert os.path.exists(source_path), f"Source file {source_path} is missing."
    assert os.path.exists(exec_path), f"Executable {exec_path} is missing."

    st = os.stat(exec_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {exec_path} is not executable."

def test_normalized_configs_output():
    input_file = '/home/user/config_events.csv'
    output_file = '/home/user/normalized_configs.csv'

    assert os.path.exists(input_file), f"Input file {input_file} is missing."
    assert os.path.exists(output_file), f"Output file {output_file} is missing."

    expected_lines = get_expected_output(input_file)

    actual_lines = []
    with open(output_file, 'r') as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                actual_lines.append(stripped)

    assert actual_lines == expected_lines, "The contents of normalized_configs.csv do not match the expected output."