# test_final_state.py
import os
import subprocess
import random
import string
import json

def test_fuzz_equivalence():
    agent_script = "/home/user/process_telemetry.py"
    oracle_script = "/app/oracle_processor.py"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_script), f"Oracle script not found at {oracle_script}"

    # Generate 5000 lines of randomized JSON-lines inputs
    random.seed(1337)
    lines = []
    for _ in range(5000):
        choice = random.random()
        if choice < 0.5:
            # Valid JSON with unicode escapes in keys and values
            x = random.randint(-1000, 1000)
            y = random.randint(-1000, 1000)
            s = f'{{"c\\u006Fordinates": {{"x": {x}, "y": {y}}}, "val": "t\\u0065st"}}'
        elif choice < 0.7:
            # Invalid JSON due to unquoted raw unicode escape that becomes valid when decoded
            x = random.randint(-1000, 1000)
            y = random.randint(-1000, 1000)
            s = f'{{"coordinates": {{"x": {x}, "y": {y}}}, "broken": \\u0022value\\u0022 }}'
        elif choice < 0.8:
            # Invalid JSON due to unquoted raw unicode escape that remains invalid
            x = random.randint(-1000, 1000)
            y = random.randint(-1000, 1000)
            s = f'{{"coordinates": {{"x": {x}, "y": {y}}}, "broken": \\u0041 }}'
        elif choice < 0.9:
            # Missing coordinates
            s = f'{{"other_data": {{"x": 1, "y": 2}}}}'
        else:
            # Random garbage
            s = "".join(random.choices(string.ascii_letters + "{}[],:\\\" ", k=random.randint(50, 200)))
        lines.append(s)

    input_data = "\n".join(lines) + "\n"

    # Run the oracle
    oracle_proc = subprocess.run(
        ["python3", oracle_script],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr}"

    # Run the agent's script
    agent_proc = subprocess.run(
        ["python3", agent_script],
        input=input_data,
        text=True,
        capture_output=True
    )

    if agent_proc.returncode != 0:
        assert False, f"Agent script failed with return code {agent_proc.returncode}\nStderr: {agent_proc.stderr}"

    agent_out = agent_proc.stdout.strip().split('\n') if agent_proc.stdout.strip() else []
    oracle_out = oracle_proc.stdout.strip().split('\n') if oracle_proc.stdout.strip() else []

    assert len(agent_out) == len(oracle_out), f"Output line count mismatch. Expected {len(oracle_out)}, got {len(agent_out)}. Are you silently dropping invalid lines as requested?"

    for i, (a, o) in enumerate(zip(agent_out, oracle_out)):
        assert a == o, f"Mismatch at output line {i+1}:\nExpected: {o}\nGot:      {a}"