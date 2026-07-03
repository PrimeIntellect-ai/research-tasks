# test_final_state.py
import os
import subprocess

def test_regression_script():
    regression_script = '/home/user/regression.sh'
    assert os.path.exists(regression_script), f"{regression_script} does not exist."
    assert os.access(regression_script, os.X_OK), f"{regression_script} is not executable."

    result = subprocess.run([regression_script], capture_output=True, text=True)
    assert "PASS" in result.stdout, f"Expected 'PASS' in output of {regression_script}, got: {result.stdout}"

def test_skipped_log():
    skipped_log = '/home/user/skipped.log'
    assert os.path.exists(skipped_log), f"{skipped_log} was not created."

    with open(skipped_log, 'r') as f:
        content = f.read().strip()

    expected_content = "SKIPPED: 30,20,50"
    assert expected_content in content, f"Expected '{expected_content}' in {skipped_log}, got: '{content}'"

    # Ensure no other rows were skipped incorrectly
    lines = [line for line in content.split('\n') if line.strip()]
    assert len(lines) == 1, f"Expected exactly 1 skipped row in {skipped_log}, but found {len(lines)}"

def test_calculate_risk_script_success():
    script_path = '/home/user/calculate_risk.sh'
    assert os.path.exists(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Remove skipped.log to ensure the script regenerates it properly
    if os.path.exists('/home/user/skipped.log'):
        os.remove('/home/user/skipped.log')

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed with exit code {result.returncode}. Stderr: {result.stderr}"

    # Verify skipped log was regenerated correctly
    skipped_log = '/home/user/skipped.log'
    assert os.path.exists(skipped_log), f"{skipped_log} was not created after running {script_path}."
    with open(skipped_log, 'r') as f:
        content = f.read().strip()
    assert "SKIPPED: 30,20,50" in content, f"Validation logic in {script_path} failed to skip the correct row."