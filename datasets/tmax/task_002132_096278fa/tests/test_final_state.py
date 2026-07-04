# test_final_state.py

import os
import subprocess
import random
import pytest

def generate_timestamps(n):
    random.seed(42)
    timestamps = []
    for _ in range(n):
        year = random.randint(1970, 2030)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        base = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"

        has_frac = random.choice([True, False])
        if has_frac:
            # Random length of fractional seconds from 1 to 6
            frac_len = random.randint(1, 6)
            frac = random.randint(0, (10**frac_len) - 1)
            base += f".{frac:0{frac_len}d}"

        tz_type = random.choice(["Z", "offset", "none"])
        if tz_type == "Z":
            base += "Z"
        elif tz_type == "offset":
            sign = random.choice(["+", "-"])
            tz_h = random.randint(0, 14)
            tz_m = random.choice([0, 30, 45])
            base += f"{sign}{tz_h:02d}:{tz_m:02d}"

        timestamps.append(base)
    return timestamps

def run_cmd(cmd, input_arg):
    try:
        # 2 second timeout to catch infinite loops
        result = subprocess.run(
            cmd + [input_arg],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT", "TIMEOUT"

def test_fuzz_equivalence():
    oracle_cmd = ["/app/parse_logs_oracle"]
    agent_cmd = ["python3", "/app/parse_logs.py"]

    assert os.path.isfile(oracle_cmd[0]), f"Oracle binary not found at {oracle_cmd[0]}"
    assert os.path.isfile(agent_cmd[1]), f"Agent script not found at {agent_cmd[1]}"

    timestamps = generate_timestamps(200)

    for ts in timestamps:
        oracle_rc, oracle_out, oracle_err = run_cmd(oracle_cmd, ts)
        agent_rc, agent_out, agent_err = run_cmd(agent_cmd, ts)

        if agent_out == "TIMEOUT":
            pytest.fail(f"Agent script timed out (infinite loop) on input: {ts}")

        assert agent_rc == oracle_rc, f"Return code mismatch on input {ts}. Oracle: {oracle_rc}, Agent: {agent_rc}\nOracle err: {oracle_err}\nAgent err: {agent_err}"

        if oracle_rc == 0:
            assert agent_out == oracle_out, f"Output mismatch on input {ts}.\nOracle: {oracle_out}\nAgent:  {agent_out}"