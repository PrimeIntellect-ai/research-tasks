# test_final_state.py
import os
import subprocess
import pytest

def test_deliverables_exist():
    """Check if all required deliverables are present."""
    expected_files = [
        '/home/user/etl_pipeline/clean_extract.c',
        '/home/user/etl_pipeline/aggregate.c',
        '/home/user/etl_pipeline/Makefile',
        '/home/user/etl_pipeline/run.sh'
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Missing deliverable: {f}"

def test_run_sh_executable():
    """Check if run.sh is executable."""
    assert os.access('/home/user/etl_pipeline/run.sh', os.X_OK), "/home/user/etl_pipeline/run.sh is not executable"

def test_pipeline_execution_and_output():
    """Compile, run the pipeline, and verify the output."""
    # Ensure it compiles
    make_result = subprocess.run(['make'], cwd='/home/user/etl_pipeline', capture_output=True, text=True)
    assert make_result.returncode == 0, f"make failed:\n{make_result.stderr}\n{make_result.stdout}"

    # Remove existing output to ensure run.sh actually creates it
    output_file = '/home/user/aggregated_stats.csv'
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the pipeline
    run_result = subprocess.run(['./run.sh'], cwd='/home/user/etl_pipeline', capture_output=True, text=True)
    assert run_result.returncode == 0, f"run.sh failed:\n{run_result.stderr}\n{run_result.stdout}"

    assert os.path.isfile(output_file), f"{output_file} was not created by run.sh"

    with open(output_file, 'r') as f:
        content = f.read().strip()

    expected = (
        "hour,total_events,error_count,avg_msg_len\n"
        "2023-10-15 14,3,1,23.33\n"
        "2023-10-15 15,2,1,17.00"
    )

    assert content.splitlines() == expected.splitlines(), (
        f"The output of the pipeline does not match the expected aggregated stats.\n"
        f"Expected:\n{expected}\n\nActual:\n{content}"
    )