# test_final_state.py

import os
import subprocess
import time
import random
import pytest

def generate_test_data(num_samples=500000):
    """
    Generates a dataset of encrypted tokens and keys.
    Returns the dataset as a single string and a set of expected hex ciphertexts
    that contain 'escalation=granted'.
    """
    lines = []
    expected = set()

    # Pre-encode keys to save time
    keys = [f"sec_{i}".encode() for i in range(10)]

    for i in range(num_samples):
        is_pos = random.random() < 0.1
        key_bytes = keys[i % 10]
        key_str = key_bytes.decode()

        if is_pos:
            pt = f"prefix_escalation=granted_{i}_suffix".encode()
        else:
            pt = f"prefix_escalation=denied_{i}_suffix".encode()

        ct_bytes = bytearray()
        for j, b in enumerate(pt):
            # Reverse of: plaintext[i] = (ciphertext[i] - (i % 256)) ^ key[i % key.length()]
            # ciphertext[i] = (plaintext[i] ^ key[i % key.length()]) + (i % 256)
            ct_b = ((b ^ key_bytes[j % len(key_bytes)]) + (j % 256)) % 256
            ct_bytes.append(ct_b)

        hex_ct = ct_bytes.hex()
        lines.append(f"{hex_ct} {key_str}\n")

        if is_pos:
            expected.add(hex_ct)

    return "".join(lines), expected

def evaluate_f1(agent_output_file, expected_set):
    try:
        with open(agent_output_file, 'r') as f:
            agent_out = set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return 0.0

    tp = len(agent_out.intersection(expected_set))
    fp = len(agent_out - expected_set)
    fn = len(expected_set - agent_out)

    if tp == 0:
        return 0.0

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1

def test_fast_auditor_performance_and_accuracy():
    binary_path = "/home/user/fast_auditor"
    input_file = "/tmp/hidden_eval_tokens.txt"
    output_file = "/tmp/agent_output.txt"

    # 1. Check if binary exists and is executable
    assert os.path.exists(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

    # 2. Generate test data
    num_samples = 500000
    data_str, expected_set = generate_test_data(num_samples)

    with open(input_file, 'w') as f:
        f.write(data_str)

    # Ensure output file is clean
    if os.path.exists(output_file):
        os.remove(output_file)

    # 3. Execute the agent's binary and measure performance
    start_time = time.time()
    try:
        result = subprocess.run(
            [binary_path, input_file, output_file],
            capture_output=True,
            text=True,
            timeout=10.0
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Execution timed out. The C++ program took more than 10 seconds.")

    execution_time = time.time() - start_time

    assert result.returncode == 0, f"Binary execution failed with return code {result.returncode}.\nSTDERR: {result.stderr}"

    # 4. Evaluate Accuracy (F1-score)
    f1_score = evaluate_f1(output_file, expected_set)

    # 5. Assertions
    assert f1_score >= 1.0, f"Accuracy failed: F1-score is {f1_score:.4f}, expected >= 1.0"
    assert execution_time < 2.0, f"Performance failed: Execution took {execution_time:.4f} seconds, expected < 2.0 seconds"