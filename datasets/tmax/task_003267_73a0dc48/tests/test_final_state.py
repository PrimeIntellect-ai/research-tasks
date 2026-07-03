# test_final_state.py

import os
import subprocess
import pytest

def test_video_incident_analysis():
    timestamps_file = "/home/user/502_timestamps.txt"
    assert os.path.isfile(timestamps_file), f"Expected file {timestamps_file} to exist."

    try:
        with open(timestamps_file, "r") as f:
            pred = [float(line.strip()) for line in f if line.strip()]
    except Exception as e:
        pytest.fail(f"Could not parse {timestamps_file} as floats: {e}")

    gt = [12.0, 24.0, 37.0, 45.0, 58.0]
    matched_gt = set()
    tp = 0
    for p in pred:
        for i, g in enumerate(gt):
            if i not in matched_gt and abs(p - g) <= 1.0:
                tp += 1
                matched_gt.add(i)
                break

    fp = len(pred) - tp
    fn = len(gt) - tp

    if tp == 0:
        f1 = 0.0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.85, f"F1 score for timestamp detection is {f1:.3f}, expected >= 0.85. Pred: {pred}"

def test_k8s_operator_fix():
    operator_script = "/home/user/k8s_operator.py"
    assert os.path.isfile(operator_script), f"Operator script {operator_script} is missing."

    # Ensure configs dir exists for the script to write to
    configs_dir = "/home/user/configs"
    os.makedirs(configs_dir, exist_ok=True)

    # Run the operator
    result = subprocess.run(["/usr/bin/python3", operator_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Operator script failed with error: {result.stderr}"

    conf_file = "/home/user/configs/app1.conf"
    assert os.path.isfile(conf_file), f"Expected generated config file {conf_file} is missing."

    with open(conf_file, "r") as f:
        content = f.read()

    expected_line = "proxy_pass http://unix:/var/run/custom-app.sock;"
    assert expected_line in content, f"Expected '{expected_line}' in {conf_file}, but got:\n{content}"

def test_setup_env_idempotency_and_cron():
    setup_script = "/home/user/setup_env.sh"
    assert os.path.isfile(setup_script), f"Setup script {setup_script} is missing."
    assert os.access(setup_script, os.X_OK), f"Setup script {setup_script} must be executable."

    configs_dir = "/home/user/configs"
    os.makedirs(configs_dir, exist_ok=True)

    # Create a dummy file to check if it gets cleared
    dummy_file = os.path.join(configs_dir, "dummy.txt")
    with open(dummy_file, "w") as f:
        f.write("test")

    # Run setup script first time
    res1 = subprocess.run(["bash", setup_script], capture_output=True, text=True)
    assert res1.returncode == 0, f"Setup script failed: {res1.stderr}"

    # Check if dummy file was cleared
    assert not os.path.exists(dummy_file), f"Setup script did not clear existing files in {configs_dir}."

    # Run setup script second time for idempotency check
    res2 = subprocess.run(["bash", setup_script], capture_output=True, text=True)
    assert res2.returncode == 0, f"Setup script failed on second run: {res2.stderr}"

    # Check crontab
    cron_res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    cron_output = cron_res.stdout.strip()

    expected_cron_job = "*/3 * * * * /usr/bin/python3 /home/user/k8s_operator.py"

    assert expected_cron_job in cron_output, f"Expected cron job '{expected_cron_job}' not found in crontab:\n{cron_output}"

    # Check for duplicates
    cron_lines = [line.strip() for line in cron_output.split("\n") if line.strip()]
    job_count = cron_lines.count(expected_cron_job)
    assert job_count == 1, f"Setup script is not idempotent. Found {job_count} instances of the cron job in crontab."