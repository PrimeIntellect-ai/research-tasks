# test_final_state.py
import os
import sys
import json
import uuid
import random
import subprocess
import tempfile
import pytest

def test_etl_pipeline_fuzz_equivalence():
    agent_script = "/home/user/etl_pipeline.py"
    oracle_script = "/app/oracle_etl_pipeline.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} does not exist."

    random.seed(42)
    num_tests = 50  # Using 50 to ensure tests run in a reasonable time

    for i in range(num_tests):
        num_rows = random.randint(10, 1000)

        # Generate product IDs
        product_ids = [str(uuid.uuid4()) for _ in range(num_rows)]

        # Generate CSV data
        csv_lines = ["product_id,quantity"]
        for pid in product_ids:
            if random.random() < 0.05:
                quantity = ""
            else:
                quantity = str(random.randint(0, 1000))
            csv_lines.append(f"{pid},{quantity}")
        csv_content = "\n".join(csv_lines)

        # Generate JSON data
        # Shuffle product IDs and maybe add some extra or remove some to test inner join
        json_pids = product_ids[:]
        random.shuffle(json_pids)

        json_data = []
        for pid in json_pids:
            price = round(random.uniform(1.0, 500.0), 2)
            json_data.append({"product_id": pid, "price": price})

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f_csv:
            f_csv.write(csv_content)
            csv_path = f_csv.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f_json:
            json.dump(json_data, f_json)
            json_path = f_json.name

        try:
            # Run oracle
            oracle_proc = subprocess.run(
                [sys.executable, oracle_script, csv_path, json_path],
                capture_output=True,
                text=True
            )

            # Run agent
            agent_proc = subprocess.run(
                [sys.executable, agent_script, csv_path, json_path],
                capture_output=True,
                text=True
            )

            # If oracle fails, skip or fail? Oracle should not fail on valid generated data.
            assert oracle_proc.returncode == 0, f"Oracle failed on input {i}:\n{oracle_proc.stderr}"

            assert agent_proc.returncode == 0, f"Agent script failed on input {i}:\n{agent_proc.stderr}"

            oracle_out = oracle_proc.stdout.strip()
            agent_out = agent_proc.stdout.strip()

            if oracle_out != agent_out:
                pytest.fail(
                    f"Mismatch on test {i} with {num_rows} rows.\n"
                    f"CSV Path: {csv_path}\n"
                    f"JSON Path: {json_path}\n"
                    f"Oracle output: {oracle_out}\n"
                    f"Agent output:  {agent_out}\n"
                )
        finally:
            os.remove(csv_path)
            os.remove(json_path)