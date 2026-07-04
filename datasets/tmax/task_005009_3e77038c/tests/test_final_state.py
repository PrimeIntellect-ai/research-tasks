# test_final_state.py
import os
import stat
import random
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/process_configs.sh"
ORACLE_SCRIPT = "/oracle/process_configs_oracle.sh"

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    st = os.stat(AGENT_SCRIPT)
    assert st.st_mode & stat.S_IXUSR, f"Agent script {AGENT_SCRIPT} is not executable."

def generate_jsonl(num_lines):
    lines = []
    for _ in range(num_lines):
        metric = "memory_weight" if random.random() < 0.5 else "cpu_limit"
        value = random.randint(10, 10000)
        if random.random() < 0.5:
            host = f"srv-\\u{random.randint(0, 65535):04x}"
        else:
            host = f"srv-{random.randint(1, 100)}"

        line = f'{{"timestamp": 1700000000, "host": "{host}", "metric": "{metric}", "value": {value}}}'
        lines.append(line)
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script {ORACLE_SCRIPT} missing."

    random.seed(42)
    for i in range(100):
        num_lines = random.randint(50, 500)
        input_data = generate_jsonl(num_lines)

        oracle_proc = subprocess.run(
            [ORACLE_SCRIPT],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"

        agent_proc = subprocess.run(
            [AGENT_SCRIPT],
            input=input_data,
            text=True,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed on iteration {i} with exit code {agent_proc.returncode}.\nStderr: {agent_proc.stderr}")

        if agent_proc.stdout != oracle_proc.stdout:
            pytest.fail(
                f"Output mismatch on iteration {i}.\n"
                f"Input sample:\n{input_data[:200]}...\n"
                f"Expected output sample:\n{oracle_proc.stdout[:200]}...\n"
                f"Agent output sample:\n{agent_proc.stdout[:200]}..."
            )