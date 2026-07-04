# test_final_state.py

import os
import json
import time
import subprocess
import pytest

def test_delivery_accuracy():
    # Determine which script exists
    script_path = None
    if os.path.isfile("/home/user/mail_router.py"):
        script_path = "/home/user/mail_router.py"
        cmd_prefix = ["python3", script_path]
    elif os.path.isfile("/home/user/mail_router.sh"):
        script_path = "/home/user/mail_router.sh"
        cmd_prefix = ["bash", script_path]
    else:
        pytest.fail("Neither /home/user/mail_router.py nor /home/user/mail_router.sh was found.")

    test_cases = [
        {"sender": "alice", "body": "test_payload_1", "expected_port": 5001},
        {"sender": "charlie", "body": "test_payload_2", "expected_port": 5002},
        {"sender": "bob", "body": "test_payload_3", "expected_port": 5001},
        {"sender": "dave", "body": "test_payload_4", "expected_port": 5002},
    ]

    correct = 0
    total = len(test_cases)

    for tc in test_cases:
        payload_dict = {"sender": tc["sender"], "body": tc["body"]}
        payload_str = json.dumps(payload_dict)

        try:
            subprocess.run(
                cmd_prefix, 
                input=payload_str.encode('utf-8'), 
                timeout=2,
                check=True
            )
            time.sleep(0.5)

            log_file = f"/tmp/backend_{tc['expected_port']}.log"
            if os.path.isfile(log_file):
                with open(log_file, "r") as f:
                    logs = f.read()
                    if payload_str in logs:
                        correct += 1
        except Exception as e:
            pass

    accuracy = correct / total
    assert accuracy >= 1.0, f"Delivery accuracy is {accuracy}, expected >= 1.0. Correctly routed: {correct}/{total}"