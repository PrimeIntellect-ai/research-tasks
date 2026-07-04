# test_final_state.py
import os
import csv
from collections import defaultdict
from datetime import datetime

def test_c_program_exists():
    path = "/home/user/aggregate.c"
    assert os.path.exists(path), f"C program {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_pipeline_script_exists_and_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.exists(path), f"Bash script {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."
    assert os.access(path, os.X_OK), f"Bash script {path} is not executable."

def test_daily_velocity_output():
    log_path = "/home/user/loc_events.log"
    output_path = "/home/user/daily_velocity.csv"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    seen_hashes = set()
    aggregated = defaultdict(int)

    with open(log_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            ts, h, lang, words = int(row[0]), row[1], row[2], int(row[3])
            if h not in seen_hashes:
                seen_hashes.add(h)
                dt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
                aggregated[(dt, lang)] += words

    expected = sorted([(k[0], k[1], v) for k, v in aggregated.items()])
    expected_lines = [f"{date},{lang},{words}" for date, lang, words in expected]

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The output in daily_velocity.csv does not match the expected aggregated data. Ensure duplicates are ignored (only the first occurrence counts) and it is sorted correctly."