# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

AGENT_SCRIPT = "/home/user/fast_processor.py"
ORACLE_BINARY = "/app/legacy_processor"

def generate_random_csv(file_path, num_rows, num_sensors, missing_rate):
    sensors = [f"sensor_{''.join(random.choices(string.ascii_lowercase, k=5))}" for _ in range(num_sensors)]

    with open(file_path, 'w') as f:
        f.write("timestamp," + ",".join(sensors) + "\n")

        timestamp = random.randint(0, 100000)

        # We need to guarantee some missing at edges and consecutive missing
        for i in range(num_rows):
            timestamp += random.randint(1, 10)
            row = [str(timestamp)]
            for j in range(num_sensors):
                # Force missing at edges for some sensors
                if (i == 0 or i == num_rows - 1) and random.random() < 0.5:
                    row.append("")
                    continue

                if random.random() < missing_rate:
                    row.append("")
                else:
                    val = random.uniform(-1000.0, 1000.0)
                    row.append(f"{val:.6f}")
            f.write(",".join(row) + "\n")


def test_fast_processor_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"


@pytest.mark.parametrize("i", range(20))
def test_fuzz_equivalence(i):
    random.seed(42 + i)

    num_rows = random.randint(100, 10000)
    num_sensors = random.randint(3, 20)
    missing_rate = random.uniform(0.05, 0.30)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_csv = os.path.join(tmpdir, "input.csv")
        oracle_out = os.path.join(tmpdir, "oracle_out.csv")
        agent_out = os.path.join(tmpdir, "agent_out.csv")

        generate_random_csv(input_csv, num_rows, num_sensors, missing_rate)

        # Run oracle
        oracle_cmd = [ORACLE_BINARY, input_csv, oracle_out]
        try:
            subprocess.run(oracle_cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on test {i}:\n{e.stderr}")

        # Run agent
        agent_cmd = ["python3", AGENT_SCRIPT, input_csv, agent_out, "--workers", "2"]
        try:
            subprocess.run(agent_cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on test {i}:\n{e.stderr}\n{e.stdout}")

        assert os.path.exists(agent_out), "Agent did not produce an output file."

        with open(oracle_out, 'r') as f1, open(agent_out, 'r') as f2:
            oracle_content = f1.read()
            agent_content = f2.read()

        if oracle_content != agent_content:
            # Output a snippet of the difference
            oracle_lines = oracle_content.splitlines()
            agent_lines = agent_content.splitlines()

            diff_idx = -1
            for idx, (ol, al) in enumerate(zip(oracle_lines, agent_lines)):
                if ol != al:
                    diff_idx = idx
                    break

            if diff_idx == -1 and len(oracle_lines) != len(agent_lines):
                diff_idx = min(len(oracle_lines), len(agent_lines))

            error_msg = f"Output mismatch on test {i} (rows={num_rows}, sensors={num_sensors}).\n"
            error_msg += f"First difference at line {diff_idx + 1}:\n"
            if diff_idx < len(oracle_lines):
                error_msg += f"Oracle: {oracle_lines[diff_idx]}\n"
            else:
                error_msg += f"Oracle: <EOF>\n"

            if diff_idx < len(agent_lines):
                error_msg += f"Agent : {agent_lines[diff_idx]}\n"
            else:
                error_msg += f"Agent : <EOF>\n"

            pytest.fail(error_msg)