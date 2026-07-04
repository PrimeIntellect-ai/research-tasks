# test_final_state.py

import os
import sys
import subprocess
import binascii
import importlib.util

def load_monitor():
    spec = importlib.util.spec_from_file_location("monitor", "/home/user/monitor.pyc")
    monitor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(monitor)
    return monitor

def test_payload_txt_exists_and_triggers_crash():
    payload_path = "/home/user/payload.txt"
    assert os.path.isfile(payload_path), f"Expected payload file at {payload_path} does not exist."

    with open(payload_path, "r") as f:
        hex_str = f.read().strip()

    assert hex_str, "payload.txt is empty."

    try:
        payload = binascii.unhexlify(hex_str)
    except Exception as e:
        assert False, f"Failed to decode hex string in payload.txt: {e}"

    monitor = load_monitor()

    exception_triggered = False
    try:
        monitor.process_heartbeat(payload)
    except RuntimeError as e:
        if str(e) == "Panic on unwrap()":
            exception_triggered = True
        else:
            assert False, f"Triggered RuntimeError but with unexpected message: {e}"
    except Exception as e:
        assert False, f"Triggered unexpected exception: {e}"

    assert exception_triggered, "The payload in payload.txt did not trigger the expected RuntimeError."

def test_regression_test_script():
    script_path = "/home/user/regression_test.py"
    assert os.path.isfile(script_path), f"Expected regression test script at {script_path} does not exist."

    # Run the script and check output
    result = subprocess.run(
        [sys.executable, script_path],
        cwd="/home/user",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"regression_test.py failed with return code {result.returncode}. Stderr: {result.stderr}"
    assert "REPRODUCED" in result.stdout, "regression_test.py did not print 'REPRODUCED' to standard output."