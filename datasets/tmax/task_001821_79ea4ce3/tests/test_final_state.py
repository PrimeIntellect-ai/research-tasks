# test_final_state.py

import os
import random
import string
import subprocess
import pytest

MASTER_PIN = 7392
ORACLE_PATH = "/app/oracle_check_auth"
AGENT_PATH = "/home/user/check_auth"

def generate_test_cases(n=5000):
    random.seed(42)
    cases = []
    # 50% valid
    for _ in range(n // 2):
        userid = random.randint(1, 1000000)
        timestamp = random.randint(1, 1000000)
        signature = (userid * 3) + timestamp + MASTER_PIN
        cases.append(f"{userid}-{timestamp}-{signature}")

    # 50% invalid / malformed
    for _ in range(n - (n // 2)):
        choice = random.randint(0, 5)
        if choice == 0:
            # wrong signature
            userid = random.randint(1, 1000000)
            timestamp = random.randint(1, 1000000)
            signature = (userid * 3) + timestamp + MASTER_PIN + random.choice([-1, 1]) * random.randint(1, 100)
            cases.append(f"{userid}-{timestamp}-{signature}")
        elif choice == 1:
            # negative numbers
            userid = random.randint(-1000, -1)
            timestamp = random.randint(1, 1000)
            signature = (userid * 3) + timestamp + MASTER_PIN
            cases.append(f"{userid}-{timestamp}-{signature}")
        elif choice == 2:
            # random string
            cases.append("".join(random.choices(string.ascii_letters + string.digits + "-", k=random.randint(5, 50))))
        elif choice == 3:
            # very long string (test buffer overflow)
            cases.append("9" * random.randint(100, 500))
        elif choice == 4:
            # non-numeric parts
            cases.append(f"{random.randint(1,100)}-ABC-{random.randint(1,100)}")
        else:
            # extra parts
            cases.append(f"10-20-30-40")

    random.shuffle(cases)
    return cases

def run_executable(path, arg):
    try:
        result = subprocess.run(
            [path, arg],
            capture_output=True,
            text=True,
            timeout=1
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT", ""
    except Exception as e:
        return -1, f"ERROR: {str(e)}", ""

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Expected executable at {AGENT_PATH} is missing."
    assert os.access(AGENT_PATH, os.X_OK), f"Expected file at {AGENT_PATH} to be executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle not executable at {ORACLE_PATH}"

    test_cases = generate_test_cases(5000)

    for i, case in enumerate(test_cases):
        oracle_code, oracle_out, _ = run_executable(ORACLE_PATH, case)
        agent_code, agent_out, _ = run_executable(AGENT_PATH, case)

        assert oracle_out == agent_out, (
            f"Mismatch on test case {i+1}/{len(test_cases)}.\n"
            f"Input: {case!r}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output: {agent_out!r}"
        )