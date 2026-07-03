# test_final_state.py
import os
import time
import requests
import pytest

def test_poison_pill_contents():
    pill_path = '/home/user/poison_pill.txt'
    assert os.path.isfile(pill_path), f"File {pill_path} does not exist."

    with open(pill_path, 'r') as f:
        poison_pill = f.read().strip()

    assert poison_pill == '3,"charlie,300', f"Poison pill content is incorrect. Expected '3,\"charlie,300', got '{poison_pill}'"

def test_server_processes_poison_pill_without_hanging():
    pill_path = '/home/user/poison_pill.txt'

    # Fallback if the file wasn't created correctly but we still want to test the server
    if os.path.isfile(pill_path):
        with open(pill_path, 'r') as f:
            poison_pill = f.read().strip()
    else:
        poison_pill = '3,"charlie,300'

    # Ensure we use the correct poison pill for the server test
    if not poison_pill:
        poison_pill = '3,"charlie,300'

    start_time = time.time()
    try:
        resp = requests.post('http://127.0.0.1:8080/process', data=poison_pill, timeout=2)
        elapsed = time.time() - start_time

        assert resp.status_code == 200, f"Expected HTTP 200, but got {resp.status_code}. Response: {resp.text}"
        assert elapsed < 1.0, f"Request took too long ({elapsed:.2f}s). The infinite loop might not be fixed."

    except requests.exceptions.Timeout:
        pytest.fail("Server timed out. The infinite loop bug is likely not fixed.")
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server at 127.0.0.1:8080. Is it running?")