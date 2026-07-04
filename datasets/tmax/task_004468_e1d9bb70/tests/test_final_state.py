# test_final_state.py

import os
import subprocess
import random
import pytest

def generate_fuzz_input():
    num_lines = random.randint(0, 500)
    lines = []
    metrics = ['YAVG', 'TEMP', 'PRES', 'VOLT', 'A', 'b', 'c']
    for _ in range(num_lines):
        if random.random() < 0.8:
            # Valid line
            frame = random.randint(0, 10000)
            metric = random.choice(metrics)
            if random.random() < 0.5:
                val = str(random.randint(0, 255))
            else:
                val = str(round(random.uniform(0.0, 255.0), 3))
            lines.append(f"{frame},{metric},{val}")
        else:
            # Invalid line
            bad_type = random.randint(0, 4)
            if bad_type == 0:
                lines.append(f"bad,YAVG,10")
            elif bad_type == 1:
                lines.append(f"15,YAVG-2,10")
            elif bad_type == 2:
                lines.append(f"16,YAVG,10.0.0")
            elif bad_type == 3:
                lines.append(f"12 YAVG 10")
            else:
                lines.append(f"12,YAVG123,10.5")
    if not lines:
        return ""
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_detector.py"
    agent_path = "/home/user/detector.py"

    assert os.path.exists(oracle_path), f"Oracle script not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent script not found at {agent_path}"

    random.seed(42)
    N = 1000

    for _ in range(N):
        inp = generate_fuzz_input()

        oracle_proc = subprocess.run(
            ["python3", oracle_path],
            input=inp,
            text=True,
            capture_output=True
        )

        agent_proc = subprocess.run(
            ["python3", agent_path],
            input=inp,
            text=True,
            capture_output=True
        )

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Stdout mismatch on input:\n{inp}\n"
            f"Oracle stdout:\n{oracle_proc.stdout}\n"
            f"Agent stdout:\n{agent_proc.stdout}"
        )

        assert oracle_proc.stderr == agent_proc.stderr, (
            f"Stderr mismatch on input:\n{inp}\n"
            f"Oracle stderr:\n{oracle_proc.stderr}\n"
            f"Agent stderr:\n{agent_proc.stderr}"
        )

def test_pipeline_output_files_exist():
    report_path = "/home/user/final_report.txt"
    error_log_path = "/home/user/pipeline_errors.log"

    assert os.path.exists(report_path), f"Expected standard output file {report_path} is missing."
    assert os.path.exists(error_log_path), f"Expected standard error file {error_log_path} is missing."