# test_final_state.py

import os
import stat
import subprocess
import tempfile
import pytest

def test_fuzzer_script_exists():
    fuzzer_path = "/home/user/fuzzer.sh"
    assert os.path.isfile(fuzzer_path), f"Fuzzer script not found at {fuzzer_path}"

def test_repro_db_exists():
    repro_path = "/home/user/repro_db.txt"
    assert os.path.isfile(repro_path), f"Reproducible DB not found at {repro_path}"

def test_resolve_deps_executable():
    script_path = "/home/user/resolve_deps.sh"
    assert os.path.isfile(script_path), f"Missing file: {script_path}"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File is not executable: {script_path}"

def test_circular_dependency_handling():
    script_path = "/home/user/resolve_deps.sh"

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("A:B\nB:C\nC:A\n")
        db_path = f.name

    try:
        result = subprocess.run(
            [script_path, "A", db_path],
            capture_output=True,
            text=True
        )

        assert result.returncode == 1, f"Expected exit code 1 for circular dependency, got {result.returncode}"
        assert "Error: Circular dependency detected for A" in result.stderr, "Expected correct error message in stderr"
    finally:
        os.remove(db_path)

def test_normal_dependency_handling():
    script_path = "/home/user/resolve_deps.sh"

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("X:Y\nY:Z\nZ:\n")
        db_path = f.name

    try:
        result = subprocess.run(
            [script_path, "X", db_path],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Expected exit code 0 for normal dependency, got {result.returncode}"
    finally:
        os.remove(db_path)

def test_repro_db_triggers_cycle():
    script_path = "/home/user/resolve_deps.sh"
    repro_path = "/home/user/repro_db.txt"

    if not os.path.isfile(repro_path):
        pytest.skip("repro_db.txt not found")

    # Read the repro DB to find a target to test
    targets = []
    with open(repro_path, 'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                targets.append(line.split(':')[0])

    assert targets, "repro_db.txt is empty or improperly formatted"

    cycle_detected = False
    for target in targets:
        result = subprocess.run(
            [script_path, target, repro_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 1 and "Error: Circular dependency detected" in result.stderr:
            cycle_detected = True
            break

    assert cycle_detected, "repro_db.txt did not trigger a circular dependency error for any of its targets"