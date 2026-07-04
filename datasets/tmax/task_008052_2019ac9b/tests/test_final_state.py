# test_final_state.py

import os
import re
import struct
import pytest

def to_f32(val):
    """Simulate 32-bit float precision."""
    return struct.unpack('f', struct.pack('f', val))[0]

def compute_expected_final_state(data_path):
    """Compute the expected mu and var sequentially from the CSV file."""
    mu = to_f32(0.0)
    var = to_f32(1.0)
    var_v = to_f32(2.0)

    w_x = to_f32(0.5)
    w_y = to_f32(0.5)
    w_z = to_f32(0.707)

    with open(data_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(',')
            x = to_f32(float(parts[0]))
            y = to_f32(float(parts[1]))
            z = to_f32(float(parts[2]))

            v = to_f32(to_f32(w_x * x) + to_f32(w_y * y) + to_f32(w_z * z))

            new_mu = to_f32(to_f32(mu * var_v + v * var) / to_f32(var + var_v))
            new_var = to_f32(to_f32(var * var_v) / to_f32(var + var_v))

            mu = new_mu
            var = new_var

    return mu, var

def test_run_sh_exists_and_executable():
    """Check that run.sh exists and is executable."""
    script_path = '/home/user/run.sh'
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_rust_project_exists():
    """Check that the Rust project was created in /home/user/etl."""
    cargo_toml_path = '/home/user/etl/Cargo.toml'
    assert os.path.exists(cargo_toml_path), f"Rust project not found. Expected {cargo_toml_path}."

def test_output_file_exists():
    """Check that output.txt was generated."""
    output_path = '/home/user/output.txt'
    assert os.path.exists(output_path), f"{output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_output_content():
    """Check that output.txt contains the correctly computed final state."""
    output_path = '/home/user/output.txt'
    data_path = '/home/user/sensor_data.csv'

    assert os.path.exists(output_path), "Cannot check content, output.txt missing."
    assert os.path.exists(data_path), "Cannot compute expected state, sensor_data.csv missing."

    expected_mu, expected_var = compute_expected_final_state(data_path)

    with open(output_path, 'r') as f:
        content = f.read().strip()

    # The expected format is exactly: Final State: mu={mu}, var={var}
    # Rounded to 4 decimal places
    expected_string = f"Final State: mu={expected_mu:.4f}, var={expected_var:.4f}"

    assert content == expected_string, (
        f"Output content mismatch.\n"
        f"Expected: '{expected_string}'\n"
        f"Got: '{content}'"
    )