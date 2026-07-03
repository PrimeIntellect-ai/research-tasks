# test_final_state.py

import os
import json
import subprocess
import pytest

def test_timeline_output_exists_and_sorted():
    output_path = "/home/user/timeline_output.json"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} is not valid JSON.")

    assert isinstance(data, list), f"{output_path} must contain a JSON array."

    # Verify all expected valid entries are present
    expected_services = ["C", "B", "A", "B", "C", "A"]
    expected_msgs = [
        "Bad timezone start",
        "Init",
        "Booting up",
        "Normal",
        "Normal message",
        "Processing"
    ]

    assert len(data) == 6, f"Expected 6 valid log entries in the timeline, found {len(data)}."

    # Extract timestamps to check sorting
    timestamps = [entry.get("timestamp") for entry in data]

    # Check if sorted
    sorted_timestamps = sorted(timestamps)
    assert timestamps == sorted_timestamps, "The timeline output is not sorted chronologically by timestamp."

    # Check content matches expected order
    for i, entry in enumerate(data):
        assert entry.get("service") == expected_services[i], f"Expected service {expected_services[i]} at index {i}, got {entry.get('service')}"
        assert entry.get("msg") == expected_msgs[i], f"Expected msg '{expected_msgs[i]}' at index {i}, got {entry.get('msg')}"

def test_corrupted_lines_log():
    log_path = "/home/user/corrupted_lines.log"
    assert os.path.isfile(log_path), f"Expected corrupted lines log {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    expected_lines = [
        '{"timestamp": "2023-10-25T14:32:00Z", "service": "B", "msg": "Missing bracket"',
        '{corrupted nonsense line}'
    ]

    assert len(lines) == 2, f"Expected 2 corrupted lines, found {len(lines)}."
    assert lines[0] == expected_lines[0], "First corrupted line does not match."
    assert lines[1] == expected_lines[1], "Second corrupted line does not match."

def test_mre_compiles_and_panics():
    mre_path = "/home/user/mre.rs"
    assert os.path.isfile(mre_path), f"MRE file {mre_path} does not exist."

    # Compile the MRE
    compile_cmd = ["rustc", mre_path, "-o", "/home/user/mre_bin"]
    # We need to link chrono, but since we are just compiling a standalone file, 
    # the student might have included it or just wrote code that fails to compile without Cargo.
    # The prompt says "It should compile with standard rustc (assuming chrono is available) and panic when executed."
    # Wait, compiling with `rustc` directly when depending on `chrono` requires passing `--extern`.
    # Let's check if it compiles via Cargo or directly. If it requires chrono, maybe we should just run it if they made it a cargo project, or compile it by finding the chrono rlib.
    # Actually, the simplest way is to check if it contains the panic string or just run `rustc` if they didn't use external crates in a way that breaks.
    # Wait, the prompt says "It should compile with standard rustc (assuming chrono is available) and panic when executed."
    # Let's try to compile it. If it fails, maybe we can just check the source code for the string and panic, or run it via a temporary cargo project.

    # Let's create a temporary cargo project to run the MRE safely with chrono dependency.
    temp_cargo_dir = "/tmp/mre_test_project"
    os.makedirs(f"{temp_cargo_dir}/src", exist_ok=True)

    with open(f"{temp_cargo_dir}/Cargo.toml", "w") as f:
        f.write("""[package]
name = "mre_test"
version = "0.1.0"
edition = "2021"

[dependencies]
chrono = "0.4"
""")

    # Copy mre.rs to main.rs
    with open(mre_path, "r") as src, open(f"{temp_cargo_dir}/src/main.rs", "w") as dst:
        dst.write(src.read())

    # Compile and run
    result = subprocess.run(
        ["cargo", "run"],
        cwd=temp_cargo_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode != 0, "MRE executed successfully, but it was expected to panic."
    assert "panic" in result.stderr.lower(), "MRE failed, but did not panic as expected."
    assert "2023-10-25T14:30:00Z+00:00" in open(mre_path).read(), "MRE does not contain the target string."