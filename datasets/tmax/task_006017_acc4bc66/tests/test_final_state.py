# test_final_state.py

import os
import subprocess
import pytest

def get_expected_results():
    """
    Dynamically calculate the expected top IP and its total bytes
    using the real tcpdump, ensuring we match the system's exact behavior.
    """
    cmd = ["/usr/sbin/tcpdump", "-nn", "-r", "/home/user/traffic.pcap"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    ip_totals = {}
    for line in result.stdout.splitlines():
        if "IP " in line:
            parts = line.split()
            try:
                ip_idx = parts.index("IP")
                src_ip_port = parts[ip_idx + 1]
                # Extract IP (remove port)
                src_ip = ".".join(src_ip_port.split(".")[:4])

                # Parse length
                if "length" in parts:
                    len_idx = parts.index("length")
                    # Strip any trailing colons or commas
                    length_str = parts[len_idx + 1].strip(":,")
                    length = int(length_str)
                    ip_totals[src_ip] = ip_totals.get(src_ip, 0) + length
            except (ValueError, IndexError):
                continue

    if not ip_totals:
        # Fallback to the truth defaults if pcap is empty or missing
        return "10.0.0.5", 272

    top_ip = max(ip_totals, key=ip_totals.get)
    return top_ip, ip_totals[top_ip]

def test_report_content_correct():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Missing {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) >= 3, f"Report file {report_path} must have at least 3 lines. Found {len(lines)} lines."

    assert lines[0] == "PACKET_CACHE", f"Line 1 (leaking array name) is incorrect. Expected 'PACKET_CACHE', got '{lines[0]}'"

    expected_ip, expected_bytes = get_expected_results()

    assert lines[1] == expected_ip, f"Line 2 (top source IP) is incorrect. Expected '{expected_ip}', got '{lines[1]}'"
    assert lines[2] == str(expected_bytes), f"Line 3 (total bytes for top IP) is incorrect. Expected '{expected_bytes}', got '{lines[2]}'"

def test_environment_fixed():
    env_path = "/home/user/env.sh"
    assert os.path.isfile(env_path), f"Missing {env_path}"

    # Check if the bad tcpdump is still being resolved first in the PATH
    cmd = ["bash", "-c", f"source {env_path} && which tcpdump"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    resolved_tcpdump = result.stdout.strip()
    assert "/home/user/bad_bin/tcpdump" not in resolved_tcpdump, (
        "The environment misconfiguration is not fixed. "
        "`which tcpdump` still resolves to the malicious mock intercepting the length field."
    )