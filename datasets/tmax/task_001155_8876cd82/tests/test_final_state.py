# test_final_state.py
import os
import subprocess
import json

def test_recovered_b_log():
    path = "/home/user/recovered_b.log"
    assert os.path.isfile(path), f"File {path} is missing. You need to extract the logs to this file."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 4, f"Expected at least 4 log entries in {path}, found {len(lines)}."

    # Check if they are valid JSONs and contain Node-B
    for line in lines:
        try:
            data = json.loads(line)
            assert data.get("service") == "Node-B", f"Expected service 'Node-B' in recovered logs, got {data.get('service')}."
        except json.JSONDecodeError:
            pytest.fail(f"Line in {path} is not valid JSON: {line}")

def test_bug_tx_txt():
    path = "/home/user/bug_tx.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "tx-8083", f"Expected 'tx-8083' in {path}, but got '{content}'."

def test_verify_loss_sh():
    script_path = "/home/user/verify_loss.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Create temporary mock logs to test the script robustly
    mock_a = "/tmp/mock_a.log"
    mock_b = "/tmp/mock_b.log"

    with open(mock_a, "w") as fa:
        fa.write('{"timestamp": "2023-10-27T08:12:01Z", "service": "Python-A", "tx_id": "tx-1", "amount": 100.0}\n')
        fa.write('{"timestamp": "2023-10-27T08:14:22Z", "service": "Python-A", "tx_id": "tx-2", "amount": 200.5555}\n')

    with open(mock_b, "w") as fb:
        fb.write('{"timestamp": "2023-10-27T08:12:03Z", "service": "Node-B", "tx_id": "tx-1", "amount": 100.0}\n')
        fb.write('{"timestamp": "2023-10-27T08:14:24Z", "service": "Node-B", "tx_id": "tx-2", "amount": 200.555}\n')

    try:
        result = subprocess.run(
            [script_path, mock_a, mock_b],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        assert output == "tx-2", f"Expected script to output 'tx-2' for mock data, but got '{output}'."
    except subprocess.CalledProcessError as e:
        assert False, f"Script execution failed with error: {e.stderr}"
    finally:
        if os.path.exists(mock_a):
            os.remove(mock_a)
        if os.path.exists(mock_b):
            os.remove(mock_b)