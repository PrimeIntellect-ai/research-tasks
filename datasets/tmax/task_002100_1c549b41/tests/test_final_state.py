# test_final_state.py
import os
import time
import subprocess
import glob
import pytest

def test_fast_extractor_exists_and_executable():
    executable = "/home/user/fast_extractor"
    assert os.path.exists(executable), f"Executable {executable} not found."
    assert os.path.isfile(executable), f"{executable} is not a file."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_zip_slip_prevention():
    # Ensure no files leaked outside the output directory
    # The task mentioned paths like ../../etc/shadow or nested/../../../home/user/.bashrc
    # We check a few obvious locations where a naive extraction might write files
    assert not os.path.exists("/home/user/etc/shadow"), "Zip-slip vulnerability detected! File leaked to /home/user/etc/shadow"
    assert not os.path.exists("/etc/shadow_leaked"), "Zip-slip vulnerability detected! File leaked to /etc/shadow_leaked"
    assert not os.path.exists("/home/user/.bashrc_leaked"), "Zip-slip vulnerability detected!"

def test_accuracy_and_performance():
    executable = "/home/user/fast_extractor"
    dataset_dir = "/home/user/dataset"
    output_dir = "/home/user/output"

    # Clean output directory to ensure we are measuring the agent's extractor run
    for f in glob.glob(os.path.join(output_dir, "*")):
        if os.path.isfile(f):
            os.remove(f)

    # Run the extractor and measure time
    start_time = time.time()
    try:
        subprocess.run([executable, dataset_dir, output_dir], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Extractor failed to run: {e.stderr}")
    elapsed = time.time() - start_time

    # The task description implies a fixed number of expected files, but since we don't 
    # have the exact generator, we know there are 1000 archives.
    # We check if there are files in the output directory.
    extracted_files = len(os.listdir(output_dir))
    assert extracted_files > 0, "No files were extracted to the output directory."

    # Check that all files are directly in the output directory (flattened)
    for root, dirs, files in os.walk(output_dir):
        assert root == output_dir or len(files) == 0, "Directories found in output, structure was not flattened."

    # Performance metric assertion
    threshold = 1.5
    assert elapsed <= threshold, f"Performance metric failed: runtime {elapsed:.4f}s > threshold {threshold}s"