# test_final_state.py
import os
import subprocess
import random
import string
import tempfile

AGENT_SCRIPT = "/home/user/config_manager.py"
ORACLE_SCRIPT = "/tmp/oracle_config_manager.py"
NUM_TESTS = 100

def generate_random_string(min_len=3, max_len=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(min_len, max_len)))

def generate_fuzz_input():
    num_ops = random.randint(5, 50)
    lines = []
    existing_keys = []

    for _ in range(num_ops):
        op_type = random.choices(["WRITE", "ALIAS", "SNAPSHOT"], weights=[70, 20, 10])[0]

        if op_type == "WRITE":
            key = generate_random_string()
            encoding = random.choice(['UTF-8', 'UTF-16LE', 'ISO-8859-1'])
            text = generate_random_string(5, 20)
            hex_payload = text.encode(encoding).hex()
            lines.append(f"WRITE {key} {encoding} {hex_payload}")
            existing_keys.append(key)
        elif op_type == "ALIAS":
            new_key = generate_random_string()
            if existing_keys:
                existing_key = random.choice(existing_keys)
                lines.append(f"ALIAS {new_key} {existing_key}")
                existing_keys.append(new_key)
            else:
                key = generate_random_string()
                lines.append(f"ALIAS {new_key} {key}")
        elif op_type == "SNAPSHOT":
            if existing_keys:
                key = random.choice(existing_keys)
            else:
                key = generate_random_string()
            lines.append(f"SNAPSHOT {key}")

    return "\n".join(lines) + "\n"

def test_config_manager_fuzz_equivalence():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script at {AGENT_SCRIPT} is not executable"
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script missing at {ORACLE_SCRIPT}"

    random.seed(42)

    for i in range(NUM_TESTS):
        fuzz_input = generate_fuzz_input()

        with tempfile.TemporaryDirectory() as oracle_ws, tempfile.TemporaryDirectory() as agent_ws:
            oracle_proc = subprocess.run(
                [ORACLE_SCRIPT, oracle_ws],
                input=fuzz_input,
                text=True,
                capture_output=True
            )

            agent_proc = subprocess.run(
                [AGENT_SCRIPT, agent_ws],
                input=fuzz_input,
                text=True,
                capture_output=True
            )

            oracle_out = oracle_proc.stdout
            agent_out = agent_proc.stdout

            error_msg = (
                f"Mismatch on fuzz test {i+1}/{NUM_TESTS}.\n"
                f"Input:\n{fuzz_input}\n"
                f"Oracle Output:\n{oracle_out}\n"
                f"Agent Output:\n{agent_out}\n"
                f"Oracle STDERR:\n{oracle_proc.stderr}\n"
                f"Agent STDERR:\n{agent_proc.stderr}\n"
            )

            assert agent_out == oracle_out, error_msg
            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Return code mismatch. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}\n{error_msg}"
            )