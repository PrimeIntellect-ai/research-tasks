# test_final_state.py
import os
import json
from collections import defaultdict

def get_expected_hubs(log_path):
    sender_receivers = defaultdict(set)
    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if (data.get("type") == "TRANSFER" and 
                data.get("status") == "COMPLETED" and 
                data.get("amount", 0) > 50000):

                sender = data.get("sender_id")
                receiver = data.get("receiver_id")
                if sender and receiver:
                    sender_receivers[sender].add(receiver)

    counts = []
    for sender, receivers in sender_receivers.items():
        counts.append((sender, len(receivers)))

    # Sort by distinct receiver count DESC, then sender_id ASC
    counts.sort(key=lambda x: (-x[1], x[0]))

    # Skip 1st record, retrieve next 3
    result = counts[1:4]

    return [f"{sender},{count}" for sender, count in result]

def test_suspicious_hubs_csv_content():
    output_file = "/home/user/suspicious_hubs.csv"
    log_file = "/home/user/audit_logs.jsonl"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist. Did you run your script and redirect output correctly?"
    assert os.path.isfile(output_file), f"{output_file} is not a file."

    expected_lines = get_expected_hubs(log_file)

    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {output_file} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual:   {actual_lines}"
    )

def test_script_exists_and_executable():
    script_file = "/home/user/analyze_hubs.sh"

    assert os.path.exists(script_file), f"Script file {script_file} does not exist."
    assert os.path.isfile(script_file), f"{script_file} is not a file."
    assert os.access(script_file, os.X_OK), f"Script file {script_file} is not executable. Use 'chmod +x' to make it executable."