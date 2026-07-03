# test_final_state.py

import os
import subprocess
import random
import pytest

def generate_fuzz_data(num_records):
    random.seed(42)
    records = []
    for _ in range(num_records):
        choice = random.random()
        if choice < 0.4:
            # Valid complete
            records.append(f"{random.randint(0, 1000000)},{random.randint(0, 1000)},{random.randint(0, 1000)}")
        elif choice < 0.7:
            # Valid missing TempB
            records.append(f"{random.randint(0, 1000000)},{random.randint(0, 1000)},")
        elif choice < 0.8:
            # Malformed letters
            records.append(f"{random.randint(0, 100)},{random.randint(0, 100)}A,{random.randint(0, 100)}")
        elif choice < 0.9:
            # Malformed missing commas
            records.append(f"{random.randint(0, 100)}{random.randint(0, 100)}")
        else:
            # Embedded newlines or carriage returns
            records.append(f"{random.randint(0, 100)},\n{random.randint(0, 100)},\r{random.randint(0, 100)}")

    return "\n".join(records) + "\n"

def test_pipeline_exists_and_executable():
    pipeline_path = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_path), f"Pipeline script not found at {pipeline_path}"
    assert os.access(pipeline_path, os.X_OK), f"Pipeline script at {pipeline_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/bin/oracle_cleaner"
    pipeline_path = "/home/user/pipeline.sh"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"

    input_data = generate_fuzz_data(10000)

    # Run oracle
    try:
        oracle_process = subprocess.run(
            [oracle_path],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=10
        )
        oracle_output = oracle_process.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle binary failed with exit code {e.returncode}. Stderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle binary timed out.")

    # Run agent pipeline
    try:
        pipeline_process = subprocess.run(
            [pipeline_path],
            input=input_data,
            text=True,
            capture_output=True,
            check=False,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Pipeline script timed out.")

    assert pipeline_process.returncode == 0, f"Pipeline script failed with exit code {pipeline_process.returncode}. Stderr: {pipeline_process.stderr}"

    pipeline_output = pipeline_process.stdout

    if oracle_output != pipeline_output:
        # Find the first line where they differ for a helpful error message
        oracle_lines = oracle_output.splitlines()
        pipeline_lines = pipeline_output.splitlines()

        diff_msg = "Outputs do not match exactly.\n"
        for i, (o_line, p_line) in enumerate(zip(oracle_lines, pipeline_lines)):
            if o_line != p_line:
                diff_msg += f"First mismatch at output line {i+1}:\nOracle:   {o_line}\nPipeline: {p_line}\n"
                break
        else:
            if len(oracle_lines) != len(pipeline_lines):
                diff_msg += f"Different number of output lines. Oracle: {len(oracle_lines)}, Pipeline: {len(pipeline_lines)}\n"

        pytest.fail(diff_msg)