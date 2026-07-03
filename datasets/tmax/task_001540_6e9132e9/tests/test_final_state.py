# test_final_state.py

import os
import subprocess
import pytest

def test_crashing_host_extracted():
    filepath = "/home/user/crashing_host.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing. Task 1 not completed."
    with open(filepath, "r") as f:
        content = f.read().strip()
    assert content == "srv-092.prod.internal", f"Expected hostname 'srv-092.prod.internal', but found '{content}' in {filepath}."

def test_makefile_dependency_conflict_resolved():
    filepath = "/home/user/uptime_project/Makefile"
    assert os.path.isfile(filepath), f"File {filepath} is missing."
    with open(filepath, "r") as f:
        content = f.read()
    assert "-I./modern_headers" in content, "Makefile does not contain the modern headers include path (-I./modern_headers). Task 2 not completed."
    assert "-I./legacy_headers" not in content, "Makefile still contains the legacy headers include path (-I./legacy_headers)."

def test_binary_compiled_and_executable():
    filepath = "/home/user/uptime_project/uptime_monitor"
    assert os.path.isfile(filepath), f"Compiled binary {filepath} is missing. Task 4 not completed."
    assert os.access(filepath, os.X_OK), f"File {filepath} is not executable."

def test_sla_calculation_fixed():
    filepath = "/home/user/uptime_project/uptime_monitor"
    assert os.path.isfile(filepath), f"Compiled binary {filepath} is missing."

    # Run the binary with arguments 99 100 0
    try:
        result = subprocess.run([filepath, "99", "100", "0"], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {filepath} failed with error: {e}")
    except Exception as e:
        pytest.fail(f"Failed to run {filepath}: {e}")

    assert output == "99.00", f"Expected output '99.00', but got '{output}'. The integer division bug in calculate_sla might not be fixed correctly. Task 3 not completed."

    # Test another case to be sure
    try:
        result2 = subprocess.run([filepath, "45", "50", "0"], capture_output=True, text=True, check=True)
        output2 = result2.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {filepath} failed with error: {e}")

    assert output2 == "90.00", f"Expected output '90.00' for inputs 45 50 0, but got '{output2}'."