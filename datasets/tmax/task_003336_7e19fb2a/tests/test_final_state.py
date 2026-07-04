# test_final_state.py

import os
import subprocess
import pytest

def test_filelock_fixed_and_installed():
    """Verify that the filelock package was fixed and installed correctly."""
    try:
        import filelock
    except ImportError:
        pytest.fail("The 'filelock' package is not installed or importable.")

    lock_path = "/tmp/test_final_state.lock"
    if os.path.exists(lock_path):
        os.remove(lock_path)

    try:
        lock = filelock.FileLock(lock_path)
        lock.acquire()
    except AttributeError as e:
        pytest.fail(f"filelock still has the AttributeError (likely O_EXCLL typo not fixed): {e}")
    except Exception as e:
        pytest.fail(f"filelock acquire failed with unexpected error: {e}")
    finally:
        if os.path.exists(lock_path):
            os.remove(lock_path)

def test_curate_script_clean_corpus(tmp_path):
    """Verify that the curate.py script successfully processes the clean corpus."""
    script_path = "/home/user/curate.py"
    assert os.path.isfile(script_path), f"Curation script not found at {script_path}"

    clean_input = "/app/verifier_corpus/clean"
    clean_out = str(tmp_path / "clean_out")
    clean_log = str(tmp_path / "clean_log.csv")

    # Run the script
    result = subprocess.run(
        ["python", script_path, "--input", clean_input, "--output", clean_out, "--log", clean_log],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Script failed on clean corpus. Stderr:\n{result.stderr}"

    # Check outputs
    expected_out_dir = os.path.join(clean_out, "abc_v9")
    assert os.path.isdir(expected_out_dir), "Clean bundle 'b1' was not moved to the expected output directory 'abc_v9'."

    # Verify the meta.json is present in the output
    assert os.path.isfile(os.path.join(expected_out_dir, "dir", "meta.json")), "Contents of the clean bundle were not preserved."

    # Check log
    assert os.path.isfile(clean_log), "Log file was not created for clean corpus."
    with open(clean_log, "r") as f:
        content = f.read().strip()

    assert "abc,9,b1" in content, f"Log file missing expected record for clean bundle. Log content:\n{content}"

def test_curate_script_evil_corpus(tmp_path):
    """Verify that the curate.py script successfully rejects the evil corpus."""
    script_path = "/home/user/curate.py"
    assert os.path.isfile(script_path), f"Curation script not found at {script_path}"

    evil_input = "/app/verifier_corpus/evil"
    evil_out = str(tmp_path / "evil_out")
    evil_log = str(tmp_path / "evil_log.csv")

    # Run the script
    result = subprocess.run(
        ["python", script_path, "--input", evil_input, "--output", evil_out, "--log", evil_log],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Script crashed or hung on evil corpus. Stderr:\n{result.stderr}"

    # Check outputs
    if os.path.exists(evil_out):
        moved_files = os.listdir(evil_out)
        assert not moved_files, f"Evil bundles were moved to output directory instead of being rejected: {moved_files}"

    # Check log
    if os.path.exists(evil_log):
        with open(evil_log, "r") as f:
            content = f.read().strip()
        assert not content, f"Log file contains entries for evil bundles:\n{content}"