# test_final_state.py

import os
import subprocess
import tempfile

def test_stats_output_file_content():
    output_file = "/home/user/monitor/stats_output.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 2, f"Output file {output_file} does not contain enough lines."
    assert "Mean: 100000000.004" in content[0], f"Expected Mean: 100000000.004, but got {content[0]}"
    assert "StdDev: 0.003" in content[1], f"Expected StdDev: 0.003, but got {content[1]}"

def test_script_robustness_on_new_data():
    script_path = "/home/user/monitor/calc_stats.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Create a new dataset with even larger base values to test numerical stability
    test_data = [
        "10000000000.001",
        "10000000000.005",
        "10000000000.002",
        "10000000000.008",
        "10000000000.004",
        "10000000000.006"
    ]

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write("\n".join(test_data) + "\n")
        tmp_path = tmp.name

    try:
        result = subprocess.run([script_path, tmp_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed with return code {result.returncode}. Error: {result.stderr}"

        output = result.stdout.strip().split('\n')
        assert len(output) >= 2, "Script did not output both Mean and StdDev."
        assert "Mean: 10000000000.004" in output[0], f"Expected Mean: 10000000000.004, but got {output[0]}"
        assert "StdDev: 0.003" in output[1], f"Expected StdDev: 0.003, but got {output[1]}"
    finally:
        os.remove(tmp_path)