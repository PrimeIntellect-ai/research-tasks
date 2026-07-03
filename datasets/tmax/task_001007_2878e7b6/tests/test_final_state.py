# test_final_state.py

import os
import re
import time
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Pipeline script {script_path} is not executable."

def test_makefile_fixed():
    makefile_path = "/app/seqcalc-1.0/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-fopenmp" in content, "Makefile does not contain '-fopenmp'. The OpenMP flag was not added."

def test_pipeline_execution_time_and_output():
    script_path = "/home/user/pipeline.sh"
    output_file = "/home/user/stats_result.txt"

    # Remove output file if it exists to ensure we are testing the script's output
    if os.path.exists(output_file):
        os.remove(output_file)

    start_time = time.time()
    try:
        subprocess.run([script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Pipeline script failed with error: {e.stderr.decode()}")
    end_time = time.time()

    execution_time = end_time - start_time

    assert execution_time <= 4.0, f"Pipeline execution time was {execution_time:.2f}s, which is greater than the threshold of 4.0s. Did you recompile seqcalc with OpenMP?"

    assert os.path.isfile(output_file), f"Output file {output_file} was not created by the pipeline."

    with open(output_file, "r") as f:
        content = f.read().strip()

    # The truth value indicates: Mean: 0.501[1-3], Variance: 0.041[0-2]
    # We will use a regex to match the expected output format and approximate values.
    pattern = r"^Mean:\s*0\.501[0-9],\s*Variance:\s*0\.041[0-9]$"
    assert re.match(pattern, content), f"Output file content '{content}' does not match the expected format or values (e.g., Mean: 0.5012, Variance: 0.0411)."