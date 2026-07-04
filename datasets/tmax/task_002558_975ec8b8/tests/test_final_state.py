# test_final_state.py

import os
import time
import subprocess
import pytest

def test_expect_script_exists():
    script_path = "/opt/auto_init.exp"
    assert os.path.isfile(script_path), f"Expect script {script_path} does not exist"
    assert os.access(script_path, os.X_OK) or "expect" in open(script_path).read(), f"{script_path} does not appear to be a valid expect script"

def test_service_file_updated():
    service_path = "/etc/systemd/system/log-archiver.service"
    assert os.path.isfile(service_path), f"Service file {service_path} does not exist"

    with open(service_path, "r") as f:
        content = f.read()

    assert "auto_init.exp" in content, "The log-archiver.service was not updated to use the expect script (/opt/auto_init.exp)"

def test_service_execution_success():
    # Since it's a oneshot service, we verify its success by checking if the backup directory and output file were created
    backup_file = "/backup/messages.lz4"
    assert os.path.isfile(backup_file), f"The service did not run successfully; expected output {backup_file} is missing"

def test_summary_file_exists():
    summary_path = "/var/log/archiver_fix_summary.txt"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} was not created"
    assert os.path.getsize(summary_path) > 0, f"Summary file {summary_path} is empty"

def test_lz4_performance_metric():
    lz4_bin = "/usr/local/bin/lz4"
    assert os.path.isfile(lz4_bin), f"Compiled binary {lz4_bin} does not exist"
    assert os.access(lz4_bin, os.X_OK), f"Compiled binary {lz4_bin} is not executable"

    input_file = "/tmp/test50m.bin"
    output_file = "/tmp/test50m.lz4"

    # Generate a 50MB random binary file
    with open(input_file, "wb") as f:
        f.write(os.urandom(50 * 1024 * 1024))

    # Measure execution time
    start_time = time.perf_counter()
    res = subprocess.run([lz4_bin, "-f", input_file, output_file], capture_output=True)
    end_time = time.perf_counter()

    assert res.returncode == 0, f"lz4 execution failed with error: {res.stderr.decode('utf-8', errors='ignore')}"
    assert os.path.isfile(output_file), f"lz4 failed to create the output file {output_file}"

    execution_time = end_time - start_time
    threshold = 1.0

    assert execution_time < threshold, (
        f"Performance metric failed: lz4 execution time was {execution_time:.3f} seconds, "
        f"which is >= the threshold of {threshold} seconds. The C code or Makefile optimization bug is not fully fixed."
    )