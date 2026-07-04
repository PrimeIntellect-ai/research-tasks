# test_final_state.py

import os
import subprocess

def test_files_exist():
    assert os.path.isfile("/home/user/extractor.c"), "/home/user/extractor.c is missing"
    assert os.path.isfile("/home/user/Makefile"), "/home/user/Makefile is missing"
    assert os.path.isfile("/home/user/run_pipeline.sh"), "/home/user/run_pipeline.sh is missing"

def test_run_pipeline_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.access(script_path, os.X_OK), f"{script_path} does not have executable permissions"

def test_pipeline_execution_and_output():
    # Remove the output file and executable if they exist to ensure the script builds and runs them
    if os.path.exists("/home/user/amplicon_data.csv"):
        os.remove("/home/user/amplicon_data.csv")
    if os.path.exists("/home/user/extractor"):
        os.remove("/home/user/extractor")

    # Run the pipeline
    result = subprocess.run(
        ["/home/user/run_pipeline.sh"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"run_pipeline.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Check if output file was created
    csv_path = "/home/user/amplicon_data.csv"
    assert os.path.isfile(csv_path), f"{csv_path} was not created by the pipeline"

    # Verify CSV contents
    expected_csv = (
        "SeqID,AmpliconLength,GC_Content\n"
        "Read_001,9,0.67\n"
        "Read_002,8,0.00\n"
        "Read_003,7,1.00"
    )

    with open(csv_path, "r") as f:
        actual_csv = f.read().strip()

    assert actual_csv == expected_csv, f"Contents of {csv_path} do not match the expected output.\nExpected:\n{expected_csv}\n\nActual:\n{actual_csv}"