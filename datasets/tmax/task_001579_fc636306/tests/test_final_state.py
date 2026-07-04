# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_C_CODE = """
#include <stdio.h>
#include <stdlib.h>

int main() {
    long long user_sums[1000] = {0}; // Assuming max user ID is well within bounds
    int uid, tid, amt;
    while (scanf("%d %d %d", &uid, &tid, &amt) == 3) {
        if (uid >= 0 && uid < 1000) {
            user_sums[uid] += amt;
            int flag = (user_sums[uid] > 5000) ? 1 : 0;
            printf("%d %d %lld %d\\n", uid, tid, user_sums[uid], flag);
        }
    }
    return 0;
}
"""

ORACLE_SRC = "/tmp/oracle_audit_query.c"
ORACLE_BIN = "/opt/oracle_audit_query"
AGENT_BIN = "/home/user/audit_query"

@pytest.fixture(scope="session", autouse=True)
def setup_oracle():
    # Write oracle source
    with open(ORACLE_SRC, "w") as f:
        f.write(ORACLE_C_CODE)

    # Compile oracle
    compile_cmd = ["gcc", "-O2", ORACLE_SRC, "-o", ORACLE_BIN]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to compile oracle: {result.stderr}"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_BIN), f"Agent binary {AGENT_BIN} does not exist."
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary {AGENT_BIN} is not executable."

def generate_fuzz_input(seed):
    rng = random.Random(seed)
    num_lines = rng.randint(0, 500)
    lines = []
    tid = 1000
    for _ in range(num_lines):
        uid = rng.randint(1, 20)
        amt = rng.randint(100, 3000)
        lines.append(f"{uid} {tid} {amt}")
        tid += 1
    return "\n".join(lines) + ("\n" if lines else "")

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_BIN), f"Agent binary {AGENT_BIN} missing."

    N = 1000
    for i in range(N):
        inp = generate_fuzz_input(42 + i)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_BIN],
            input=inp,
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_BIN],
            input=inp,
            capture_output=True,
            text=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent binary crashed or returned non-zero on iteration {i}.\nInput:\n{inp[:200]}...\nStderr:\n{agent_proc.stderr}")

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i}!\n"
                f"Input (first 500 chars):\n{inp[:500]}\n\n"
                f"Oracle Output (first 500 chars):\n{oracle_out[:500]}\n\n"
                f"Agent Output (first 500 chars):\n{agent_out[:500]}"
            )