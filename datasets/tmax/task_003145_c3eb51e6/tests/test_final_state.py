# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_makefile_fixed():
    """Check that the broken whitespace parsing flag is removed from the Makefile."""
    makefile_path = "/app/librouteconf-2.1.0/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile missing at {makefile_path}"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-DBROKEN_WHITESPACE_PARSING=1" not in content, "The perturbation flag -DBROKEN_WHITESPACE_PARSING=1 is still present in the Makefile."

def test_fuzz_equivalence():
    """Fuzz test the agent's route_canonicalizer against the oracle."""
    agent_bin = "/home/user/route_canonicalizer"
    oracle_bin = "/opt/oracle/route_canonicalizer"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    random.seed(42)
    valid_chars = string.ascii_letters + string.digits + " ->:,"

    for i in range(1000):
        length = random.randint(10, 500)
        is_malformed = random.random() < 0.2

        if is_malformed:
            # Inject random printable characters to ensure malformed input
            inp = "".join(random.choices(string.printable, k=length))
        else:
            # Use the specified character set
            inp = "".join(random.choices(valid_chars, k=length))

        inp_bytes = inp.encode('utf-8', errors='ignore')

        proc_oracle = subprocess.run(
            [oracle_bin],
            input=inp_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        proc_agent = subprocess.run(
            [agent_bin],
            input=inp_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert proc_oracle.returncode == proc_agent.returncode, (
            f"Exit code mismatch on input {repr(inp)}.\n"
            f"Oracle returned: {proc_oracle.returncode}\n"
            f"Agent returned: {proc_agent.returncode}"
        )

        assert proc_oracle.stdout == proc_agent.stdout, (
            f"Stdout mismatch on input {repr(inp)}.\n"
            f"Oracle stdout: {proc_oracle.stdout!r}\n"
            f"Agent stdout: {proc_agent.stdout!r}"
        )