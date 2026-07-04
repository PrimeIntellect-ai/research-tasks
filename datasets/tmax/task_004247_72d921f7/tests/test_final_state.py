# test_final_state.py

import os
import time
import subprocess
import glob

def test_archived_files():
    archive_dir = "/data/archive"
    assert os.path.isdir(archive_dir), f"The directory {archive_dir} is missing. Did you run the archival process?"

    archived_files = glob.glob(os.path.join(archive_dir, "*.archive"))
    assert len(archived_files) > 0, f"No '.archive' files found in {archive_dir}."

    for fpath in archived_files:
        with open(fpath, 'r') as f:
            for line in f:
                assert "[DEBUG]" not in line, f"Found [DEBUG] line in archived file {fpath}, filtering failed."

def test_performance_and_atomic_write():
    test_file = "/tmp/test_large.log"
    out_dir = "/tmp/archive_out"
    os.makedirs(out_dir, exist_ok=True)

    # Create dummy 50MB log file
    with open(test_file, "w") as f:
        for i in range(500000):
            if i % 5 == 0:
                f.write(f"[{i}] [DEBUG] Some debug information to filter out\n")
            else:
                f.write(f"[{i}] [INFO] Normal log line information\n")

    script_path = "/app/bash-log-archiver-1.0/archive.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Ensure script is executable
    os.chmod(script_path, 0o755)

    start = time.time()
    result = subprocess.run([script_path, test_file, out_dir], capture_output=True, text=True)
    duration = time.time() - start

    assert result.returncode == 0, f"archive.sh failed with error:\n{result.stderr}"
    assert duration <= 2.0, f"Speedup not sufficient, took {duration:.2f}s (threshold <= 2.0s)."

    # Verify the output file was created
    out_file = os.path.join(out_dir, "test_large.archive")
    assert os.path.isfile(out_file), f"Expected output file {out_file} not found. Script may not be writing to the correct destination."

    # Check atomic write implementation (heuristic: check script content for mv)
    with open(script_path, "r") as f:
        content = f.read()
        assert "mv " in content, "archive.sh does not appear to use 'mv' for atomic writes. You must write to a temp file and move it."

def test_makefile_fixed():
    makefile_path = "/app/bash-log-archiver-1.0/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} is missing."

    with open(makefile_path, "r") as f:
        content = f.read()
        assert "ARCHIVE_DIR" in content, "Makefile does not contain 'ARCHIVE_DIR'. The typo was not fixed."
        assert "DEST_DIR" not in content, "Makefile still contains 'DEST_DIR'. The typo was not fixed."