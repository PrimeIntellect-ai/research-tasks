# test_final_state.py

import os
import subprocess
import pytest

def test_detector_f1_score(tmp_path):
    detector_path = "/home/user/detector.py"
    assert os.path.isfile(detector_path), f"Detector script not found at {detector_path}"

    # Use the held-out truth file if it exists, otherwise generate a mock one
    truth_file = "/truth/held_out_auth.log"
    if os.path.isfile(truth_file):
        log_file = truth_file
        truth_ips = {"192.168.1.55", "10.0.0.9", "172.16.5.101", "198.51.100.22"}
    else:
        log_file_path = tmp_path / "auth.log"
        log_content = """
Dec 15 10:22:33 host sshd[1234]: Accepted publickey for b4ckd00r_adm1n_xyz from 192.168.1.55 port 44322 ssh2
Dec 15 10:22:35 host sshd[1235]: Invalid user admin from 10.1.2.3 port 33444
Dec 15 10:22:36 host sshd[1236]: Accepted password for b4ckd00r_adm1n_xyz from 10.0.0.9 port 55555 ssh2
Dec 15 10:22:37 host sshd[1237]: Accepted publickey for root from 192.168.1.55 port 44322 ssh2
Dec 15 10:22:38 host sshd[1238]: Accepted keyboard-interactive/pam for b4ckd00r_adm1n_xyz from 172.16.5.101 port 12345 ssh2
Dec 15 10:22:39 host sshd[1239]: Failed password for b4ckd00r_adm1n_xyz from 1.1.1.1 port 22
Dec 15 10:22:40 host sshd[1240]: Accepted publickey for b4ckd00r_adm1n_xyz from 198.51.100.22 port 2222 ssh2
"""
        log_file_path.write_text(log_content.strip() + "\n")
        log_file = str(log_file_path)
        truth_ips = {"192.168.1.55", "10.0.0.9", "172.16.5.101", "198.51.100.22"}

    try:
        out = subprocess.check_output(["python3", detector_path, log_file], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Detector script failed with error: {e}")

    agent_ips = set([line.strip() for line in out.split('\n') if line.strip()])

    tp = len(truth_ips.intersection(agent_ips))
    fp = len(agent_ips - truth_ips)
    fn = len(truth_ips - agent_ips)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.95, (
        f"F1 Score {f1:.4f} is below the threshold of 0.95. "
        f"Precision: {precision:.4f}, Recall: {recall:.4f}. "
        f"Detected IPs: {agent_ips}"
    )