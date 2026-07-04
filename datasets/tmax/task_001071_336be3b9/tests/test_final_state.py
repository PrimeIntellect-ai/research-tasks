# test_final_state.py
import json
import os
import random
import subprocess
import pytest

def generate_fuzz_input(seed: int) -> str:
    random.seed(seed)
    num_lines = random.randint(0, 500)
    lines = []
    locales = ["en-US", "fr-FR", "zh-CN", "pt-BR", "invalid-LOC"]

    current_ts = 1600000000
    for _ in range(num_lines):
        if random.random() < 0.2:
            # Generate invalid JSON or missing fields
            if random.random() < 0.5:
                lines.append("not a json line {")
            else:
                obj = {}
                if random.random() < 0.5: obj['ts'] = current_ts
                if random.random() < 0.5: obj['loc'] = random.choice(locales)
                lines.append(json.dumps(obj))
        else:
            # Generate valid JSON
            if random.random() < 0.1:
                current_ts += random.randint(1000, 5000) # Large gap
            elif random.random() < 0.3:
                current_ts += random.randint(60, 300) # Medium gap
            elif random.random() < 0.2:
                pass # Exact duplicate ts
            else:
                current_ts += random.randint(1, 59) # Small gap

            obj = {
                'ts': current_ts,
                'loc': random.choice(locales),
                'lat': random.uniform(10.0, 1000.0)
            }
            # Occasionally make values strings to test robustness
            if random.random() < 0.05:
                obj['ts'] = str(obj['ts'])
            if random.random() < 0.05:
                obj['lat'] = str(obj['lat'])

            lines.append(json.dumps(obj))

    return "\n".join(lines)

def run_script(script_path: str, input_data: str) -> dict:
    try:
        result = subprocess.run(
            ["python3", script_path],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=5
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script {script_path} failed with exit code {e.returncode}.\nStderr: {e.stderr}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Script {script_path} produced invalid JSON output.\nStdout: {result.stdout}\nError: {e}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script {script_path} timed out.")

def test_fuzz_equivalence():
    agent_script = "/home/user/process.py"
    oracle_script = "/oracle/process.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."

    N = 200
    for seed in range(N):
        input_data = generate_fuzz_input(seed)

        oracle_output = run_script(oracle_script, input_data)
        agent_output = run_script(agent_script, input_data)

        if oracle_output != agent_output:
            pytest.fail(
                f"Mismatch on seed {seed}!\n"
                f"Input lines: {len(input_data.splitlines())}\n"
                f"Oracle output: {json.dumps(oracle_output, indent=2)}\n"
                f"Agent output: {json.dumps(agent_output, indent=2)}\n"
                f"Input data:\n{input_data}"
            )