# test_final_state.py

import os
import re
from collections import defaultdict

def test_script_exists_and_executable():
    script_path = "/home/user/process_loc.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_sampled_loc_tsv_content():
    input_path = "/home/user/loc_events.tsv"
    output_path = "/home/user/sampled_loc.tsv"

    assert os.path.isfile(input_path), f"Input file {input_path} missing."
    assert os.path.isfile(output_path), f"Output file {output_path} missing."

    with open(input_path, "r", encoding="utf-8") as f:
        input_lines = f.read().splitlines()

    # Compute expected output
    parsed_records = []
    for line in input_lines:
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 4:
            parsed_records.append(parts)

    # Sort chronologically
    parsed_records.sort(key=lambda x: x[0])

    expected_records = []
    lang_counts = defaultdict(int)

    for parts in parsed_records:
        ts, email, lang, text = parts[0], parts[1], parts[2], parts[3:]

        # Mask email
        if "@" in email:
            user, domain = email.split("@", 1)
            masked_user = user[0] + "*" if len(user) > 0 else "*"
            masked_email = f"{masked_user}@{domain}"
        else:
            masked_email = email

        if lang_counts[lang] < 2:
            expected_records.append("\t".join([ts, masked_email, lang] + text))
            lang_counts[lang] += 1

    with open(output_path, "r", encoding="utf-8") as f:
        output_lines = [line for line in f.read().splitlines() if line.strip()]

    # Check that output matches expected
    assert len(output_lines) == len(expected_records), f"Expected {len(expected_records)} rows in output, but got {len(output_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_records, output_lines)):
        assert actual == expected, f"Row {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"

def test_pipeline_log_content():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} missing."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in {log_path}, got {len(lines)}."

    assert lines[0].startswith("[START]"), "First line must start with [START]."
    assert lines[3].startswith("[END]"), "Fourth line must start with [END]."

    # The input has 10 lines, output has 9 lines
    assert "[PROCESSED] 10" in lines[1] or "[PROCESSED] 10" in lines[2], "Log must contain '[PROCESSED] 10'."
    assert "[OUTPUT] 9" in lines[1] or "[OUTPUT] 9" in lines[2], "Log must contain '[OUTPUT] 9'."

    # Ensure order of PROCESSED and OUTPUT
    assert lines[1].startswith("[PROCESSED]"), "Second line must start with [PROCESSED]."
    assert lines[2].startswith("[OUTPUT]"), "Third line must start with [OUTPUT]."