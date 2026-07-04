# test_final_state.py
import os
import subprocess
import random
import time
import hashlib

def test_fuzz_equivalence():
    oracle_path = '/app/bin/oracle_ingestor'
    agent_path = '/home/user/artifact_ingestor'

    assert os.path.isfile(agent_path), f"Agent program not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program {agent_path} is not executable"

    random.seed(42)

    # Test 100 random inputs to ensure equivalence without causing timeouts
    for i in range(100):
        length = random.randint(0, 100000)
        input_data = random.randbytes(length)

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, "Oracle program failed unexpectedly"
        assert agent_proc.returncode == 0, f"Agent program crashed on input of length {length}"

        if oracle_proc.stdout != agent_proc.stdout:
            assert False, f"Output mismatch on input of length {length}. Agent output did not match Oracle."

def test_end_to_end_integration():
    incoming_dir = '/home/user/incoming'
    assert os.path.isdir(incoming_dir), f"Directory {incoming_dir} does not exist. Did you create it?"

    random.seed(time.time())
    test_filename = f"test_artifact_{random.randint(10000, 99999)}.bin"
    file_path = os.path.join(incoming_dir, test_filename)

    data = random.randbytes(50000)
    expected_hash = hashlib.sha256(data).hexdigest()

    # Drop the file into the incoming directory
    with open(file_path, 'wb') as f:
        f.write(data)

    # Wait for the watcher script to detect, process, and upload the file
    redis_cmd = ["redis-cli", "GET", f"artifact:hash:{test_filename}"]

    output = ""
    for _ in range(15):
        time.sleep(1)
        result = subprocess.run(redis_cmd, capture_output=True, text=True)
        output = result.stdout.strip()
        if output == expected_hash:
            break

    assert output == expected_hash, f"Expected hash {expected_hash} not found in Redis for key artifact:hash:{test_filename}. Got: {output}. Ensure your watcher script is running and correctly uploading the normalized data."