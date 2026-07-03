# test_final_state.py

import os
import re

def test_results_file_exists():
    assert os.path.isfile("/home/user/results.txt"), "The file /home/user/results.txt does not exist."

def test_results_content_and_value():
    with open("/home/user/results.txt", "r") as f:
        content = f.read().strip()

    match = re.search(r"Estimated k:\s*(\d+\.\d{3})", content)
    assert match is not None, f"Could not find 'Estimated k: X.XXX' in /home/user/results.txt. Content was: '{content}'"

    k_value = float(match.group(1))
    assert 0.110 <= k_value <= 0.130, f"Estimated k ({k_value}) is outside the acceptable range of [0.110, 0.130]."

def test_scripts_exist():
    bash_script = "/home/user/run_analysis.sh"
    python_script = "/home/user/fit_kinetics.py"

    assert os.path.isfile(bash_script), f"Bash script {bash_script} does not exist."
    assert os.access(bash_script, os.X_OK), f"Bash script {bash_script} is not executable."

    assert os.path.isfile(python_script), f"Python script {python_script} does not exist."