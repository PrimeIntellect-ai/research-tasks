# test_final_state.py

import os
import subprocess
import time
import pytest

def test_services_running():
    """
    Test that start_all.sh correctly starts app_server.py and cost_analyzer.py,
    and both remain running (which implies cost_analyzer.py waited for the symlink).
    """
    # Ensure a clean slate: kill existing processes and remove the symlink
    subprocess.run(["pkill", "-f", "python3 /home/user/services/app_server.py"], capture_output=True)
    subprocess.run(["pkill", "-f", "python3 /home/user/services/cost_analyzer.py"], capture_output=True)

    symlink_path = "/home/user/app_data/active_data"
    if os.path.exists(symlink_path) or os.path.islink(symlink_path):
        os.remove(symlink_path)

    script_path = "/home/user/services/start_all.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"

    # Execute the script
    subprocess.Popen(["bash", script_path], cwd="/home/user/services")

    # Wait for the app_server to create the symlink (3 seconds) + margin
    time.sleep(5)

    # Check if both processes are running
    app_server_check = subprocess.run(["pgrep", "-f", "python3 /home/user/services/app_server.py"], capture_output=True)
    cost_analyzer_check = subprocess.run(["pgrep", "-f", "python3 /home/user/services/cost_analyzer.py"], capture_output=True)

    assert app_server_check.returncode == 0, "app_server.py is not running in the background. It may have crashed or was not started."
    assert cost_analyzer_check.returncode == 0, "cost_analyzer.py is not running in the background. It likely crashed because it started before the active_data symlink was created."

def test_classifier_script():
    """
    Test the classifier script against the clean and evil corpora.
    """
    script_path = "/home/user/classifier.py"
    assert os.path.isfile(script_path), f"Classifier script missing at {script_path}"

    evil_dir = "/home/user/corpus/evil/"
    clean_dir = "/home/user/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    # Test Evil Corpus
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "DELETE":
            evil_bypassed.append(filename)

    # Test Clean Corpus
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "KEEP":
            clean_modified.append(filename)

    # Surface clear summary on failure
    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))