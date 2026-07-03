# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_filter"
AGENT_SCRIPT = "/home/user/k8s_filter.sh"
N_TESTS = 500

# Use a safe subset of printable characters to avoid weird shell reading behaviors on null bytes/VT/FF
CHARS = string.ascii_letters + string.digits + string.punctuation + " "

def generate_random_line():
    choice = random.choices(["random", "image_pull", "replicas", "abort"], weights=[70, 10, 15, 5])[0]

    if choice == "random":
        length = random.randint(0, 100)
        return "".join(random.choices(CHARS, k=length))

    elif choice == "image_pull":
        prefix = "".join(random.choices(CHARS, k=random.randint(0, 20)))
        suffix = "".join(random.choices(CHARS, k=random.randint(0, 20)))
        return f"{prefix}imagePullPolicy: Always{suffix}"

    elif choice == "replicas":
        spaces = " " * random.randint(0, 10)
        num = random.randint(0, 20)
        return f"{spaces}replicas: {num}"

    elif choice == "abort":
        return "CRITICAL_ABORT!"

def generate_input():
    lines = []
    for _ in range(random.randint(0, 50)):
        lines.append(generate_random_line())
    res = "\n".join(lines)
    # Randomly leave off the trailing newline
    if random.random() > 0.5 and res:
        res += "\n"
    return res

def test_script_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} is missing."

    random.seed(42)

    for i in range(N_TESTS):
        inp = generate_input()

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=inp,
            text=True,
            capture_output=True
        )

        agent_proc = subprocess.run(
            ["/bin/bash", AGENT_SCRIPT],
            input=inp,
            text=True,
            capture_output=True
        )

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Fuzz test {i} failed!\n"
            f"Input:\n{inp!r}\n\n"
            f"Expected Output (Oracle):\n{oracle_proc.stdout!r}\n\n"
            f"Actual Output (Agent):\n{agent_proc.stdout!r}"
        )

        # We only check exit code if it's the abort case, since the oracle exits 0 on abort.
        if "CRITICAL_ABORT!" in inp.split("\n"):
            # If the abort string is present exactly as a line, both should exit 0
            if any(line == "CRITICAL_ABORT!" for line in inp.split("\n")):
                assert agent_proc.returncode == 0, "Agent did not exit with code 0 upon receiving the termination signal."