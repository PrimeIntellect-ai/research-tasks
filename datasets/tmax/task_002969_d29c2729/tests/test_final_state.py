# test_final_state.py
import os
import sys
import subprocess
import glob
import multiprocessing
import pytest

EVIL_CORPUS_DIR = "/testdata/evil_corpus"
CLEAN_CORPUS_DIR = "/testdata/clean_corpus"
DETECTOR_SCRIPT = "/home/user/detector.py"
DPKT_PATH = "/app/dpkt-1.9.8"

def run_detector(pcap_path):
    try:
        result = subprocess.run(
            [sys.executable, DETECTOR_SCRIPT, pcap_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1

def test_detector_evil_corpus():
    assert os.path.exists(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.pcap"))
    assert len(evil_files) > 0, f"No evil pcaps found in {EVIL_CORPUS_DIR}"

    bypassed = []
    for pcap in evil_files:
        output, retcode = run_detector(pcap)
        if output != "EVIL" or retcode != 0:
            bypassed.append(os.path.basename(pcap))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_detector_clean_corpus():
    assert os.path.exists(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.pcap"))
    assert len(clean_files) > 0, f"No clean pcaps found in {CLEAN_CORPUS_DIR}"

    modified = []
    for pcap in clean_files:
        output, retcode = run_detector(pcap)
        if output != "CLEAN" or retcode != 0:
            modified.append(os.path.basename(pcap))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (failed to return CLEAN). Offending files: {', '.join(modified)}")

def parse_pcap_in_worker(pcap_path):
    sys.path.insert(0, DPKT_PATH)
    import dpkt
    with open(pcap_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if isinstance(ip.data, dpkt.tcp.TCP):
                    pass

def test_dpkt_fix_no_hang():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.pcap"))
    assert len(evil_files) > 0, f"No evil pcaps found in {EVIL_CORPUS_DIR}"

    # Just test the first few to avoid taking too long, or test all if fast
    for pcap in evil_files[:5]:
        p = multiprocessing.Process(target=parse_pcap_in_worker, args=(pcap,))
        p.start()
        p.join(timeout=2.0)

        if p.is_alive():
            p.terminate()
            p.join()
            pytest.fail(f"dpkt parsing hung on {os.path.basename(pcap)} - fix in dpkt/tcp.py is missing or incorrect.")

        # We don't assert exitcode == 0 because it might raise UnpackError which is acceptable
        # The key is that it doesn't hang.