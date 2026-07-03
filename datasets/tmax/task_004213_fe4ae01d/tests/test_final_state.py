# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def test_base_ini_recovered():
    base_ini_path = "/home/user/base.ini"
    assert os.path.exists(base_ini_path), "base.ini was not found at /home/user/base.ini"

    with open(base_ini_path, "r") as f:
        content = f.read().strip()

    expected_content = "[Core]\nVersion=1.0\n[Modules]\nAuth=true"
    assert content == expected_content, f"Content of base.ini is incorrect. Got:\n{content}"

def test_script_exists_and_no_prohibited_interpreters():
    script_path = "/home/user/apply_config.sh"
    assert os.path.exists(script_path), f"Agent script missing at {script_path}"

    with open(script_path, "r") as f:
        content = f.read().lower()

    for interpreter in ["python", "perl", "ruby", "node"]:
        assert interpreter not in content, f"Script contains prohibited interpreter: {interpreter}"

def generate_random_changelog(num_lines):
    lines = []
    sections = ["Core", "Modules", "Network", "System", "DB"]
    keys = ["Version", "Auth", "Host", "Port", "User", "Pass", "Timeout", "Retry"]

    for _ in range(num_lines):
        cmd = random.choice(["ADD", "MOD", "DEL"])
        sec = random.choice(sections) + "".join(random.choices(string.ascii_letters, k=3))
        key = random.choice(keys) + "".join(random.choices(string.ascii_letters, k=2))
        val = "".join(random.choices(string.ascii_letters + string.digits, k=6))

        if cmd == "ADD":
            lines.append(f"ADD {sec} {key} {val}")
        elif cmd == "MOD":
            lines.append(f"MOD {sec} {key} {val}")
        elif cmd == "DEL":
            lines.append(f"DEL {sec} {key}")

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_apply.sh"
    agent_path = "/home/user/apply_config.sh"

    assert os.path.exists(oracle_path), "Oracle script missing"
    assert os.path.exists(agent_path), "Agent script missing"

    random.seed(42)
    num_tests = 100

    for i in range(num_tests):
        num_lines = random.randint(10, 100)
        changelog = generate_random_changelog(num_lines)

        # Run oracle
        oracle_proc = subprocess.run(
            ["bash", oracle_path],
            input=changelog,
            text=True,
            capture_output=True
        )

        # Run agent
        agent_proc = subprocess.run(
            ["bash", agent_path],
            input=changelog,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed on test {i}\nInput:\n{changelog}\nStderr:\n{agent_proc.stderr}"
        assert oracle_proc.returncode == 0, f"Oracle script failed on test {i}"

        if agent_proc.stdout != oracle_proc.stdout:
            pytest.fail(
                f"Mismatch on test {i}!\n"
                f"Input Changelog:\n{changelog}\n"
                f"Oracle Output:\n{oracle_proc.stdout}\n"
                f"Agent Output:\n{agent_proc.stdout}"
            )