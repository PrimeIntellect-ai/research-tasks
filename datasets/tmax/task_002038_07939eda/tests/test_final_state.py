# test_final_state.py

import os
import subprocess
import struct
import math

def test_bad_commit_txt():
    """Verify that bad_commit.txt contains the correct commit hash."""
    repo_path = '/home/user/sensor_aggregator'
    bad_commit_file = '/home/user/bad_commit.txt'

    assert os.path.isfile(bad_commit_file), f"{bad_commit_file} is missing."

    # Get the actual bad commit hash
    result = subprocess.run(
        ['git', '-C', repo_path, 'log', '--grep=Add normalization based on variance', '--format=%H'],
        capture_output=True,
        text=True,
        check=True
    )
    expected_hash = result.stdout.strip()
    assert expected_hash, "Could not find the expected bad commit in the git repository."

    with open(bad_commit_file, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected commit hash {expected_hash}, but found {actual_hash} in {bad_commit_file}."

def test_poison_payload_txt():
    """Verify that poison_payload.txt contains the correct hex-encoded payload."""
    poison_file = '/home/user/poison_payload.txt'

    assert os.path.isfile(poison_file), f"{poison_file} is missing."

    # The expected poison payload is sensor_id=2, v1=15.5, v2=15.5
    expected_payload_bytes = struct.pack('<Iff', 2, 15.5, 15.5)
    expected_hex = expected_payload_bytes.hex()

    with open(poison_file, 'r') as f:
        actual_hex = f.read().strip().lower()

    assert actual_hex == expected_hex, f"Expected poison payload {expected_hex}, but found {actual_hex} in {poison_file}."

def test_fixed_aggregate_py():
    """Verify that fixed_aggregate.py correctly handles the poison payload and normal payloads."""
    fixed_script = '/home/user/fixed_aggregate.py'

    assert os.path.isfile(fixed_script), f"{fixed_script} is missing."

    # Test with poison payload
    poison_payload = struct.pack('<Iff', 2, 15.5, 15.5).hex()
    result_poison = subprocess.run(
        ['python3', fixed_script, poison_payload],
        capture_output=True,
        text=True
    )

    assert result_poison.returncode == 0, f"fixed_aggregate.py crashed with poison payload. Error: {result_poison.stderr}"

    output_poison = result_poison.stdout.strip()
    try:
        val_poison = float(output_poison)
        assert math.isclose(val_poison, 0.0), f"fixed_aggregate.py should output 0.0 for poison payload, got {val_poison}"
    except ValueError:
        assert False, f"fixed_aggregate.py produced invalid float output for poison payload: {output_poison}"

    # Test with normal payload
    normal_payload = struct.pack('<Iff', 1, 10.0, 20.0).hex()
    result_normal = subprocess.run(
        ['python3', fixed_script, normal_payload],
        capture_output=True,
        text=True
    )

    assert result_normal.returncode == 0, f"fixed_aggregate.py crashed with normal payload. Error: {result_normal.stderr}"

    output_normal = result_normal.stdout.strip()
    try:
        val_normal = float(output_normal)
        # mean = 15.0, var = ((10-15)^2 + (20-15)^2)/2 = 25.0, sqrt(var) = 5.0, normalized = 15.0 / 5.0 = 3.0
        assert math.isclose(val_normal, 3.0), f"fixed_aggregate.py produced incorrect output for normal payload: {val_normal}"
    except ValueError:
        assert False, f"fixed_aggregate.py produced invalid float output for normal payload: {output_normal}"