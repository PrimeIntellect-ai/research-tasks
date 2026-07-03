# test_final_state.py
import json
import re
import os
import pytest

def test_compliance_artifacts_score():
    """
    Evaluates the compliance JSON report and firewall script.
    Calculates a match ratio based on 5 checks.
    Requires a score of at least 0.8 (4 out of 5).
    """
    score = 0
    total = 5

    json_path = "/home/user/compliance_report.json"
    sh_path = "/home/user/firewall_update.sh"

    # Check JSON
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)

                if data.get("attacker_ip") == "10.55.20.156":
                    score += 1
                if data.get("target_port") == 443:
                    score += 1
                if str(data.get("cwe_id", "")).upper() == "CWE-78":
                    score += 1
                if data.get("decoded_payload") == "ls -la /etc/passwd":
                    score += 1
        except Exception:
            pass

    # Check Firewall Script
    if os.path.exists(sh_path):
        try:
            with open(sh_path, "r") as f:
                content = f.read()
                # Look for standard iptables drop rule
                if re.search(r"iptables\s+-A\s+INPUT\s+.*-s\s+10\.55\.20\.156.*-p\s+tcp.*--dport\s+443.*-j\s+DROP", content) or \
                   re.search(r"iptables\s+-I\s+INPUT\s+.*-s\s+10\.55\.20\.156.*-p\s+tcp.*--dport\s+443.*-j\s+DROP", content):
                    score += 1
        except Exception:
            pass

    metric = score / total
    assert metric >= 0.8, f"Score metric {metric} is below the threshold of 0.8. Score: {score}/{total}. Required at least 4/5 correct items."