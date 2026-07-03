# test_final_state.py

import os
import time
import subprocess
import zipfile
import stat
import pytest

def test_process_dataset_exists_and_executable():
    bin_path = "/home/user/process_dataset"
    assert os.path.exists(bin_path), f"The compiled binary {bin_path} does not exist."
    assert os.path.isfile(bin_path), f"{bin_path} is not a file."

    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The binary {bin_path} is not executable."

def test_process_dataset_performance_and_success():
    bin_path = "/home/user/process_dataset"

    # We remove the output files if they exist from previous runs
    for f in ["/home/user/manifest.csv", "/home/user/clean_dataset.zip"]:
        if os.path.exists(f):
            os.remove(f)

    start = time.time()
    result = subprocess.run([bin_path], capture_output=True)
    end = time.time()

    runtime = end - start

    assert result.returncode == 0, f"process_dataset failed with exit code {result.returncode}. Stderr: {result.stderr.decode('utf-8', errors='replace')}"
    assert runtime <= 1.5, f"Execution time {runtime:.2f}s exceeded the 1.5s threshold."

def test_outputs_generated_correctly():
    manifest_path = "/home/user/manifest.csv"
    zip_path = "/home/user/clean_dataset.zip"
    clean_dir = "/home/user/clean"

    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} was not generated."
    assert os.path.exists(zip_path), f"Zip archive {zip_path} was not generated."
    assert os.path.isdir(clean_dir), f"Clean directory {clean_dir} does not exist."

    with open(manifest_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) > 0, "Manifest file is empty, expected valid research data files to be found."

    # Check that zip is valid and contains files
    assert zipfile.is_zipfile(zip_path), f"{zip_path} is not a valid zip file."
    with zipfile.ZipFile(zip_path, "r") as z:
        zip_names = z.namelist()
        assert len(zip_names) > 0, "Zip archive is empty."

        # Verify that the manifest entries correspond to files in the zip
        for line in lines:
            if not line.strip():
                continue
            parts = line.split(",")
            assert len(parts) == 2, f"Invalid manifest line format: {line}"
            original_path, sha_name = parts[0].strip(), parts[1].strip()

            # The zip might contain the clean/ prefix or just the files, but the sha_name should be present
            found_in_zip = any(sha_name in z_name for z_name in zip_names)
            assert found_in_zip, f"File {sha_name} from manifest not found in the zip archive."