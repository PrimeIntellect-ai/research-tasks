# test_final_state.py

import os
import subprocess
import pytest

def test_scripts_exist_and_executable():
    """Check if optimize.sh and fast_query.sh exist and are executable."""
    scripts = ["/home/user/optimize.sh", "/home/user/fast_query.sh"]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_index_directory_and_partitions():
    """Check if the index directory and expected partition files exist."""
    index_dir = "/home/user/index"
    assert os.path.isdir(index_dir), f"Directory {index_dir} does not exist."

    # Check for specific partition files known to be generated from the injected records
    part_55 = os.path.join(index_dir, "part_55.csv")
    part_00 = os.path.join(index_dir, "part_00.csv")

    assert os.path.isfile(part_55), f"Partition file {part_55} is missing."
    assert os.path.isfile(part_00), f"Partition file {part_00} is missing."

def test_fast_query_uses_partitioning():
    """Verify that fast_query.sh contains logic to use the partition files."""
    script_path = "/home/user/fast_query.sh"
    with open(script_path, "r") as f:
        content = f.read()

    assert "part_" in content, "fast_query.sh does not appear to read from the part_XX.csv partition files."

def test_fast_query_output_cust_55555():
    """Check the fast_query.sh output for CUST-55555."""
    result = subprocess.run(["/home/user/fast_query.sh", "CUST-55555"], capture_output=True, text=True)
    assert result.returncode == 0, f"fast_query.sh failed to execute for CUST-55555. Error: {result.stderr}"

    output = result.stdout.strip()
    try:
        total = float(output)
    except ValueError:
        pytest.fail(f"fast_query.sh returned non-numeric output for CUST-55555: '{output}'")

    # Expected: 100.00 + 250.50 = 350.50 (Clothing 999.99 is ignored)
    assert abs(total - 350.50) < 0.01, f"Expected total spend of 350.50 for CUST-55555, but got {total}"

def test_fast_query_output_cust_10000():
    """Check the fast_query.sh output for CUST-10000."""
    result = subprocess.run(["/home/user/fast_query.sh", "CUST-10000"], capture_output=True, text=True)
    assert result.returncode == 0, f"fast_query.sh failed to execute for CUST-10000. Error: {result.stderr}"

    output = result.stdout.strip()
    try:
        total = float(output)
    except ValueError:
        pytest.fail(f"fast_query.sh returned non-numeric output for CUST-10000: '{output}'")

    # Expected: 50.25
    assert abs(total - 50.25) < 0.01, f"Expected total spend of 50.25 for CUST-10000, but got {total}"