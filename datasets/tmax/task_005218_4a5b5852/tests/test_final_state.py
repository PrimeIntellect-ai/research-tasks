# test_final_state.py

import os
import time
import subprocess
import glob
import shutil

def test_pipeline_execution_and_metrics():
    app_dir = "/home/user/app"
    data_dir = os.path.join(app_dir, "data")
    output_dir = os.path.join(app_dir, "output")
    supervisor_script = os.path.join(app_dir, "supervisor.sh")

    assert os.path.isfile(supervisor_script), f"Supervisor script missing at {supervisor_script}"

    # Clear data and output directories to ensure a clean run
    for dir_path in [data_dir, output_dir]:
        if os.path.exists(dir_path):
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        else:
            os.makedirs(dir_path)

    # Execute supervisor.sh and measure the duration
    start_time = time.time()
    result = subprocess.run(
        [supervisor_script],
        capture_output=True,
        text=True
    )
    end_time = time.time()

    duration = end_time - start_time

    # Ensure the script ran successfully
    assert result.returncode == 0, (
        f"supervisor.sh failed with return code {result.returncode}.\n"
        f"STDOUT: {result.stdout}\n"
        f"STDERR: {result.stderr}"
    )

    # Verify the secondary metric: Count of files in output directory
    output_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    count = len(output_files)

    assert count == 20, (
        f"Expected exactly 20 files in {output_dir}, but found {count}.\n"
        f"Files found: {output_files}"
    )

    # Verify the primary metric: Total execution time
    assert duration <= 3.5, (
        f"Pipeline execution took {duration:.3f} seconds, which exceeds the threshold of 3.5 seconds. "
        "The processor script might not be properly parallelized or the sleep mechanism is inefficient."
    )