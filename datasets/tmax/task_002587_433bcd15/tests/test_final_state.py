# test_final_state.py
import os
import subprocess

def test_bug_report_contents():
    report_path = '/home/user/bug_report.txt'
    assert os.path.isfile(report_path), f"The report file {report_path} is missing."

    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {report_path}, found {len(lines)}."

    assert lines[0] == "Failing Seed: 4", f"Expected 'Failing Seed: 4', got '{lines[0]}'"
    assert lines[1] == "Overflowed Energy: -2146914693", f"Expected 'Overflowed Energy: -2146914693', got '{lines[1]}'"
    assert lines[2] == "Correct Energy: 2148052603", f"Expected 'Correct Energy: 2148052603', got '{lines[2]}'"

def test_compute_energy_fixed():
    script_path = '/home/user/compute_energy.py'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

    # Run the script with seed 4
    result = subprocess.run(
        ['python3', script_path, '4'], 
        capture_output=True, 
        text=True
    )

    assert result.returncode == 0, f"Script failed with seed 4. Error: {result.stderr}\nOutput: {result.stdout}"
    assert "Error: Negative energy calculated!" not in result.stdout, "Script still produces negative energy error for seed 4."
    assert "Energy: 2148052603" in result.stdout, f"Script did not output the correct energy. Output was: {result.stdout}"