# test_final_state.py

import os
import subprocess
import re

def test_policy_enforcer_script_exists_and_executable():
    """Check if the agent created the policy enforcer script and made it executable."""
    script_path = '/home/user/policy_enforcer.sh'
    assert os.path.isfile(script_path), f"Agent script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Agent script {script_path} is not executable."

def test_policy_enforcer_accuracy():
    """Run the evaluation script to check the accuracy of the policy enforcer."""
    eval_script = '/eval/test_accuracy.py'
    assert os.path.isfile(eval_script), f"Evaluation script {eval_script} is missing."

    result = subprocess.run(['python3', eval_script], capture_output=True, text=True)

    # Try to parse accuracy from the output if present, otherwise rely on the return code
    accuracy_match = re.search(r'(?i)accuracy.*?([0-9]*\.?[0-9]+)', result.stdout)
    if accuracy_match:
        accuracy = float(accuracy_match.group(1))
        assert accuracy >= 0.98, f"Accuracy {accuracy} is below the threshold of 0.98. Output: {result.stdout}"
    else:
        assert result.returncode == 0, f"Accuracy test failed. Output: {result.stdout}\nError: {result.stderr}"