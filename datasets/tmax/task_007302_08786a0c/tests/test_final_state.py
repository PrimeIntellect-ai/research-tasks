# test_final_state.py
import os
import stat
import json
import subprocess
import hashlib
import pytest

def test_scripts_exist_and_executable():
    """Test that analyzer.py and run_parallel.sh exist, and run_parallel.sh is executable."""
    analyzer_path = '/home/user/analyzer.py'
    runner_path = '/home/user/run_parallel.sh'

    assert os.path.isfile(analyzer_path), f"{analyzer_path} is missing."
    assert os.path.isfile(runner_path), f"{runner_path} is missing."

    st = os.stat(runner_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{runner_path} is not executable."

def test_execution_and_manifest():
    """Test that running run_parallel.sh produces the correct dedup_manifest.json."""
    manifest_path = '/home/user/dedup_manifest.json'

    # Remove manifest if it exists to ensure the script creates it
    if os.path.exists(manifest_path):
        os.remove(manifest_path)

    # Run the bash script
    result = subprocess.run(['/home/user/run_parallel.sh'], capture_output=True, text=True)
    assert result.returncode == 0, f"run_parallel.sh failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert os.path.isfile(manifest_path), "dedup_manifest.json was not created after running run_parallel.sh"

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("dedup_manifest.json does not contain valid JSON.")

    # Compute expected hashes dynamically
    hash_A = hashlib.sha256(b"ERROR: Disk full\n").hexdigest()
    hash_B = hashlib.sha256(b"WARN: High memory usage\n").hexdigest()
    hash_C = hashlib.sha256(b"INFO: System rebooted\n").hexdigest()

    assert hash_A in manifest, f"Manifest is missing hash for content A: {hash_A}"
    assert hash_B in manifest, f"Manifest is missing hash for content B: {hash_B}"
    assert hash_C in manifest, f"Manifest is missing hash for content C: {hash_C}"

    # Expected path suffixes
    expected_A = {
        "backup1.tar/logs1.zip/logA.log",
        "backup2.tar/logs2.zip/logA_dup.log"
    }
    expected_B = {
        "backup1.tar/logs1.zip/logB.log",
        "backup3.tar/logs3.zip/logB_dup.log"
    }
    expected_C = {
        "backup2.tar/logs2.zip/logC.log"
    }

    def check_paths(actual_paths, expected_suffixes):
        for expected in expected_suffixes:
            # Check if any actual path ends with the expected suffix
            # (allowing for absolute paths like /home/user/old_backups/backup1.tar/...)
            assert any(p.endswith(expected) for p in actual_paths), \
                f"Expected path ending with '{expected}' not found in {actual_paths}"

        # Also ensure no extra paths are present
        assert len(actual_paths) == len(expected_suffixes), \
            f"Expected {len(expected_suffixes)} paths, but found {len(actual_paths)}: {actual_paths}"

    check_paths(manifest[hash_A], expected_A)
    check_paths(manifest[hash_B], expected_B)
    check_paths(manifest[hash_C], expected_C)