# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_inputs(n=2500):
    random.seed(42)
    inputs = []
    for _ in range(n):
        is_invalid = random.random() < 0.05
        if is_invalid:
            # Generate completely invalid inputs
            choices = [
                "just a string",
                "12.34",
                "12.34, 56.78, 90.12",
                "abc, def",
                "",
            ]
            inputs.append(random.choice(choices))
            continue

        lat = random.uniform(-90.0, 90.0)
        lon = random.uniform(-180.0, 180.0)
        prec1 = random.randint(1, 9)
        prec2 = random.randint(1, 9)

        s_lat = f"{lat:.{prec1}f}"
        s_lon = f"{lon:.{prec2}f}"

        is_corrupted = random.random() < 0.3

        if is_corrupted:
            # Missing leading zeros
            if random.random() < 0.5:
                if s_lat.startswith("0."):
                    s_lat = s_lat[1:]
                elif s_lat.startswith("-0."):
                    s_lat = "-" + s_lat[2:]
            if random.random() < 0.5:
                if s_lon.startswith("0."):
                    s_lon = s_lon[1:]
                elif s_lon.startswith("-0."):
                    s_lon = "-" + s_lon[2:]

            # Corrupted separators
            sep = random.choice([",", " , ", "\t,\t", ",  \t", " ,"])
            s = s_lat + sep + s_lon

            # Leading/trailing whitespaces
            if random.random() < 0.5:
                s = random.choice([" ", "\t", "  \t "]) + s
            if random.random() < 0.5:
                s = s + random.choice([" ", "\t", "  \t "])
        else:
            s = f"{s_lat}, {s_lon}"

        inputs.append(s)
    return inputs

def test_fixed_parser_fuzz_equivalence():
    agent_script = "/home/user/fixed_parser.py"
    oracle_bin = "/opt/oracle_parser"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    inputs = generate_inputs(2500)

    for inp in inputs:
        oracle_proc = subprocess.run(
            [oracle_bin, inp],
            capture_output=True,
            text=True
        )
        agent_proc = subprocess.run(
            ["python3", agent_script, inp],
            capture_output=True,
            text=True
        )

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on input: {repr(inp)}\n"
            f"Expected (Oracle): {repr(oracle_out)}\n"
            f"Got (Agent): {repr(agent_out)}"
        )