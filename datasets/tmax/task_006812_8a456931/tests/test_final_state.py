# test_final_state.py

import os
import subprocess

def test_run_pipeline_script():
    script_path = "/home/user/motif_analysis/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Execute the pipeline script to generate the output
    result = subprocess.run(
        [script_path], 
        capture_output=True, 
        text=True, 
        cwd="/home/user/motif_analysis"
    )
    assert result.returncode == 0, f"Pipeline script failed to execute. STDERR: {result.stderr}"

def test_steady_state_output():
    output_path = "/home/user/motif_analysis/steady_state.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    try:
        values = [float(x.strip()) for x in content.split(',')]
    except ValueError:
        pytest.fail("Output file does not contain valid comma-separated floats.")

    assert len(values) == 10, f"Expected exactly 10 values, but got {len(values)}."

    total_sum = sum(values)
    assert abs(total_sum - 1.0) < 1e-5, f"Probabilities must sum to 1, but sum is {total_sum}."

    assert abs(values[5] - 1.0) < 1e-5, f"State 5 must be approximately 1.0, but got {values[5]}."

    for i, val in enumerate(values):
        assert val >= -1e-7, f"Probabilities must be non-negative, but got {val} at index {i}."