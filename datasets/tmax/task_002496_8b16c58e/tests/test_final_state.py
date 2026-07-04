# test_final_state.py
import os
import subprocess
import random
import string
import pytest
from datetime import datetime, timedelta

def test_video_summary_exists_and_format():
    summary_path = "/home/user/video_summary.csv"
    assert os.path.exists(summary_path), f"Expected output file not found: {summary_path}"

    with open(summary_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, "Video summary CSV is empty."
    assert lines[0] == "BucketStart,ServerID,TotalEvents,UniqueKeys", "CSV header does not match the required format."

def generate_fuzz_input(num_lines):
    lines = []
    for _ in range(num_lines):
        is_malformed = random.random() < 0.05
        if is_malformed:
            # Generate malformed line
            bad_type = random.choice([1, 2, 3])
            if bad_type == 1:
                # Missing columns
                lines.append(" ".join("".join(random.choices(string.ascii_letters, k=5)) for _ in range(3)))
            elif bad_type == 2:
                # Bad timestamp
                lines.append(f"[2024-99-99T99:99:99Z] server UPDATE key val")
            else:
                # Random garbage
                lines.append("".join(random.choices(string.ascii_letters + string.digits + " ", k=30)))
        else:
            # Valid line
            dt = datetime(2020, 1, 1) + timedelta(seconds=random.randint(0, 5 * 365 * 24 * 3600))
            ts = dt.strftime("[%Y-%m-%dT%H:%M:%SZ]")
            server_id = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 15)))
            action = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 15)))
            key = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 15)))
            new_val = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 15)))
            lines.append(f"{ts} {server_id} {action} {key} {new_val}")
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    agent_code = "/home/user/parser.go"
    agent_bin = "/tmp/agent_parser"
    oracle_bin = "/app/oracle_parser"

    assert os.path.exists(agent_code), f"Agent code not found: {agent_code}"
    assert os.path.exists(oracle_bin), f"Oracle binary not found: {oracle_bin}"

    # Compile agent code
    compile_proc = subprocess.run(["go", "build", "-o", agent_bin, agent_code], capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Failed to compile agent code:\n{compile_proc.stderr}"

    random.seed(42)

    for i in range(100):
        num_lines = random.randint(0, 1000)
        fuzz_input = generate_fuzz_input(num_lines)

        # Run oracle
        oracle_proc = subprocess.run([oracle_bin], input=fuzz_input, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}:\n{oracle_proc.stderr}"

        # Run agent
        agent_proc = subprocess.run([agent_bin], input=fuzz_input, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent failed on iteration {i}:\n{agent_proc.stderr}"

        # Compare
        if oracle_proc.stdout != agent_proc.stdout:
            # Truncate output for error message if too long
            oracle_out = oracle_proc.stdout[:1000] + ("..." if len(oracle_proc.stdout) > 1000 else "")
            agent_out = agent_proc.stdout[:1000] + ("..." if len(agent_proc.stdout) > 1000 else "")

            pytest.fail(f"Mismatch on iteration {i} (num_lines={num_lines}).\n"
                        f"--- Expected (Oracle) ---\n{oracle_out}\n"
                        f"--- Actual (Agent) ---\n{agent_out}\n")