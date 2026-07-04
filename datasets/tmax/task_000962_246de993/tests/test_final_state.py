# test_final_state.py
import os
import subprocess
import pytest

def calculate_f1(truth, pred):
    tp = len(truth & pred)
    fp = len(pred - truth)
    fn = len(truth - pred)

    if tp == 0:
        return 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2 * (precision * recall) / (precision + recall)

def create_eval_data():
    log_path = "/home/user/eval_logs/access.log"
    truth_path = "/home/user/eval_logs/truth.txt"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logs = []
    truth_ips = set()

    # 1. Path traversal
    logs.append('192.168.1.101 - - [10/Oct/2023:13:55:36 -0700] "GET /api/data?file=../../etc/passwd HTTP/1.1" 200 512 "-" "curl/7.68.0"')
    logs.append('192.168.1.111 - - [10/Oct/2023:13:55:36 -0700] "GET /api/data?file=%2e%2e%2fetc/passwd HTTP/1.1" 200 512 "-" "curl/7.68.0"')
    truth_ips.update(["192.168.1.101", "192.168.1.111"])

    # 2. SQLi
    logs.append('192.168.1.102 - - [10/Oct/2023:13:55:37 -0700] "GET /api/data?id=1%20UNION%20SELECT%201,2,3 HTTP/1.1" 200 512 "-" "curl/7.68.0"')
    truth_ips.add("192.168.1.102")

    # 3. Command injection
    logs.append('192.168.1.103 - - [10/Oct/2023:13:55:38 -0700] "GET /api/data?cmd=;%20rm%20-rf%20/ HTTP/1.1" 200 512 "-" "curl/7.68.0"')
    logs.append('192.168.1.113 - - [10/Oct/2023:13:55:38 -0700] "GET /api/data?cmd=$(whoami) HTTP/1.1" 200 512 "-" "curl/7.68.0"')
    truth_ips.update(["192.168.1.103", "192.168.1.113"])

    # 4. >50 401 errors
    for _ in range(55):
        logs.append('192.168.1.104 - - [10/Oct/2023:13:55:39 -0700] "GET /api/data HTTP/1.1" 401 128 "-" "curl/7.68.0"')
    truth_ips.add("192.168.1.104")

    # 5. Legitimate
    logs.append('192.168.1.200 - - [10/Oct/2023:13:55:40 -0700] "GET /api/data HTTP/1.1" 200 512 "-" "curl/7.68.0"')

    # 6. Legitimate with some 401s (<50)
    for _ in range(10):
        logs.append('192.168.1.201 - - [10/Oct/2023:13:55:41 -0700] "GET /api/data HTTP/1.1" 401 128 "-" "curl/7.68.0"')

    with open(log_path, "w") as f:
        f.write("\n".join(logs) + "\n")

    with open(truth_path, "w") as f:
        f.write("\n".join(truth_ips) + "\n")

    return log_path, truth_ips

def test_ids_filter_f1_score():
    script_path = "/home/user/ids_filter.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    log_path, truth_ips = create_eval_data()
    pred_path = "/home/user/predictions.txt"

    result = subprocess.run([script_path, log_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    with open(pred_path, "w") as f:
        f.write(result.stdout)

    pred_ips = set(line.strip() for line in result.stdout.splitlines() if line.strip())

    f1 = calculate_f1(truth_ips, pred_ips)

    assert f1 >= 0.95, f"F1 score {f1:.4f} is below the threshold of 0.95. Truth: {truth_ips}, Pred: {pred_ips}"