# test_final_state.py

import os
import json
import re
from collections import defaultdict

def test_rejected_count_and_flagged_ids():
    input_file = "/home/user/loc_updates.jsonl"
    rejected_file = "/home/user/rejected_count.txt"
    flagged_file = "/home/user/flagged_ids.txt"

    assert os.path.exists(input_file), f"Input file {input_file} is missing."
    assert os.path.exists(rejected_file), f"Output file {rejected_file} is missing."
    assert os.path.exists(flagged_file), f"Output file {flagged_file} is missing."

    # Process input file to compute expected results
    rejected_count = 0
    valid_updates = []

    with open(input_file, "r") as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            lang = data.get("lang", "")
            old_str = data.get("old", "")
            new_str = data.get("new", "")

            is_valid = True
            if not re.match(r"^[a-z]{2}$", lang):
                is_valid = False
            elif not new_str:
                is_valid = False
            elif old_str == new_str:
                is_valid = False

            if not is_valid:
                rejected_count += 1
            else:
                valid_updates.append(data)

    # Group and sort
    groups = defaultdict(list)
    for update in valid_updates:
        groups[(update["lang"], update["mod"])].append(update)

    expected_flagged_ids = set()

    for group_key, items in groups.items():
        # Sort by ts, then id
        items.sort(key=lambda x: (x["ts"], x["id"]))

        rolling_window = []
        for item in items:
            old_len = len(item["old"].encode('utf-8'))
            new_len = len(item["new"].encode('utf-8'))
            r = new_len / (old_len + 1)

            rolling_window.append(r)
            if len(rolling_window) > 5:
                rolling_window.pop(0)

            avg_r = sum(rolling_window) / len(rolling_window)
            if avg_r > 2.500:
                expected_flagged_ids.add(item["id"])

    expected_flagged_ids_sorted = sorted(list(expected_flagged_ids))

    # Check rejected count
    with open(rejected_file, "r") as f:
        actual_rejected = f.read().strip()

    assert actual_rejected == str(rejected_count), f"Expected rejected_count.txt to contain '{rejected_count}', but got '{actual_rejected}'."

    # Check flagged IDs
    with open(flagged_file, "r") as f:
        actual_flagged = [line.strip() for line in f if line.strip()]

    assert actual_flagged == expected_flagged_ids_sorted, f"Expected flagged_ids.txt to contain {expected_flagged_ids_sorted}, but got {actual_flagged}."