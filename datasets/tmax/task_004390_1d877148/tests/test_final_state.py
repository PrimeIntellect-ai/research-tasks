# test_final_state.py

import os
import subprocess
import random
import tempfile
import re
import pytest

def test_artifacts_exist():
    assert os.path.exists("/home/user/libframeparser.so"), "Missing /home/user/libframeparser.so"
    assert os.path.exists("/home/user/analyzer_cli"), "Missing /home/user/analyzer_cli"
    assert os.access("/home/user/analyzer_cli", os.X_OK), "/home/user/analyzer_cli is not executable"
    assert os.path.exists("/home/user/ci_report.txt"), "Missing /home/user/ci_report.txt"

def test_fuzz_equivalence():
    oracle = "/app/oracle_analyzer"
    agent = "/home/user/analyzer_cli"

    assert os.path.exists(oracle), f"Oracle missing at {oracle}"
    assert os.path.exists(agent), f"Agent missing at {agent}"

    random.seed(42)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Run a representative sample of N iterations to avoid test timeout
        # while still providing high confidence of equivalence.
        for i in range(500):
            # Generate 12288 bytes
            data = bytearray(random.getrandbits(8) for _ in range(12288))
            with open(tmp_path, "wb") as f:
                f.write(data)

            oracle_proc = subprocess.run([oracle, tmp_path], capture_output=True, text=True)
            agent_proc = subprocess.run([agent, tmp_path], capture_output=True, text=True)

            oracle_out = oracle_proc.stdout
            agent_out = agent_proc.stdout

            assert oracle_out == agent_out, (
                f"Mismatch on fuzz iteration {i}.\n"
                f"Oracle output: {oracle_out!r}\n"
                f"Agent output: {agent_out!r}"
            )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def test_ci_report_format():
    report_path = "/home/user/ci_report.txt"
    assert os.path.exists(report_path), f"Missing {report_path}"

    with open(report_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 120, f"Expected 120 lines in ci_report.txt, got {len(lines)}"

    for i, line in enumerate(lines):
        frame_num = i + 1
        match = re.match(r'^Frame (\d+): (PASS|FAIL|FLAKY|CORRUPT)$', line)
        assert match, f"Line {i+1} does not match expected format: {line}"
        assert int(match.group(1)) == frame_num, f"Expected Frame {frame_num}, got {match.group(1)}"