# test_final_state.py

import os
import sys
import math
import subprocess
import pytest

def test_dpkt_installed_and_fixed():
    try:
        import dpkt
    except ImportError:
        pytest.fail("dpkt is not installed in the current Python environment.")

    # Create a simple valid IPv4 packet header
    # 45 00 00 14 00 01 00 00 40 00 7c e7 7f 00 00 01 7f 00 00 01
    raw_ip = bytes.fromhex("450000140001000040007ce77f0000017f000001")

    try:
        ip_obj = dpkt.ip.IP(raw_ip)
    except Exception as e:
        pytest.fail(f"Failed to parse a valid IP packet with the installed dpkt: {e}")

    assert type(ip_obj.sum) is int, f"Expected ip_obj.sum to be int, got {type(ip_obj.sum)}"
    assert not math.isnan(ip_obj.sum), "ip_obj.sum is NaN, perturbation was not fixed."

def test_detector_script_exists():
    path = "/home/user/detector.py"
    assert os.path.isfile(path), f"Detector script not found at {path}"

def test_detector_clean_corpus():
    clean_dir = "/app/corpora/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    pcap_files = [f for f in os.listdir(clean_dir) if f.endswith(".pcap")]
    assert len(pcap_files) > 0, "No pcap files found in clean corpus."

    failed_files = []
    for pcap in pcap_files:
        pcap_path = os.path.join(clean_dir, pcap)
        result = subprocess.run(
            [sys.executable, "/home/user/detector.py", pcap_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 or "CLEAN" not in result.stdout:
            failed_files.append(pcap)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(pcap_files)} clean modified/flagged. Offending files: {', '.join(failed_files)}")

def test_detector_evil_corpus():
    evil_dir = "/app/corpora/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    pcap_files = [f for f in os.listdir(evil_dir) if f.endswith(".pcap")]
    assert len(pcap_files) > 0, "No pcap files found in evil corpus."

    failed_files = []
    for pcap in pcap_files:
        pcap_path = os.path.join(evil_dir, pcap)
        result = subprocess.run(
            [sys.executable, "/home/user/detector.py", pcap_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 1 or "EVIL" not in result.stdout:
            failed_files.append(pcap)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(pcap_files)} evil bypassed. Offending files: {', '.join(failed_files)}")