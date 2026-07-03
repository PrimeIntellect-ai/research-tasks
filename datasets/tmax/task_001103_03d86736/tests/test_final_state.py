# test_final_state.py

import os
import time
import subprocess
import glob
import shutil

def test_process_all_script_exists_and_executable():
    script_path = "/home/user/process_all.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_execution_time_and_security():
    script_path = "/home/user/process_all.sh"
    processed_dir = "/home/user/processed"
    system_fake_dir = "/home/user/system_fake"

    # Clean up directories before running to ensure accurate timing and security checks
    if os.path.exists(processed_dir):
        shutil.rmtree(processed_dir)
    os.makedirs(processed_dir, exist_ok=True)

    if os.path.exists(system_fake_dir):
        shutil.rmtree(system_fake_dir)
    os.makedirs(system_fake_dir, exist_ok=True)

    # Measure execution time
    start_time = time.time()
    result = subprocess.run([script_path], capture_output=True, text=True)
    end_time = time.time()

    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    execution_time = end_time - start_time

    # Verify security constraint (tar slip prevented)
    if os.path.isdir(system_fake_dir):
        files_in_fake = os.listdir(system_fake_dir)
        assert len(files_in_fake) == 0, f"Tar slip vulnerability not fixed! Files found in {system_fake_dir}: {files_in_fake}"

    # Verify that files were actually extracted
    extracted_files = glob.glob(os.path.join(processed_dir, "**", "*"), recursive=True)
    extracted_files = [f for f in extracted_files if os.path.isfile(f)]
    assert len(extracted_files) > 0, f"No files were extracted to {processed_dir}. The script did not process the archives correctly."

    # Verify performance constraint
    assert execution_time <= 2.0, f"Execution time {execution_time:.2f}s exceeded the 2.0s threshold. Optimization may be incomplete."