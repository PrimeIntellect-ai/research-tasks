# test_final_state.py

import os
import subprocess
import random
import pytest
import time
import json
import urllib.request

def test_sim_core_fuzz_equivalence():
    agent_script = "/home/user/sim_core.py"
    oracle_script = "/app/ref_sim.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} not found."

    random.seed(1337)
    for _ in range(1000):
        N_steps = random.randint(10, 1000)
        seed = random.randint(0, 999999)
        p_right = round(random.uniform(0.1, 0.9), 3)
        L = random.randint(5, 50)

        args = [str(N_steps), str(seed), str(p_right), str(L)]

        oracle_cmd = ["python3", oracle_script] + args
        agent_cmd = ["python3", agent_script] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on args {args}"
        assert agent_res.returncode == 0, f"Agent script failed on args {args}:\n{agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on inputs N_steps={N_steps}, seed={seed}, p_right={p_right}, L={L}.\n"
            f"Expected: '{oracle_out}'\n"
            f"Got: '{agent_out}'"
        )

def test_worker_end_to_end():
    worker_script = "/home/user/worker.sh"
    assert os.path.isfile(worker_script), f"Worker script {worker_script} not found."
    assert os.access(worker_script, os.X_OK), f"Worker script {worker_script} is not executable."

    # Start the worker script in the background
    worker_proc = subprocess.Popen(["bash", worker_script])

    try:
        # Push 5 jobs to Redis
        jobs = [
            ("job1", 100, 42, 0.6, 10),
            ("job2", 200, 43, 0.5, 20),
            ("job3", 50, 44, 0.8, 5),
            ("job4", 500, 45, 0.2, 15),
            ("job5", 10, 46, 0.9, 50)
        ]

        for job in jobs:
            job_str = f"{job[0]}|{job[1]}|{job[2]}|{job[3]}|{job[4]}"
            subprocess.run(["redis-cli", "LPUSH", "job_queue", job_str], check=True)

        # Poll the Flask API /results endpoint
        success = False
        for _ in range(20):
            time.sleep(0.5)
            try:
                req = urllib.request.Request("http://localhost:5000/results")
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode('utf-8'))
                        # The API might return a list of results or a dict
                        if isinstance(data, list):
                            job_ids = {d.get("job_id") for d in data if isinstance(d, dict)}
                        elif isinstance(data, dict):
                            job_ids = set(data.keys())
                        else:
                            job_ids = set()

                        if {"job1", "job2", "job3", "job4", "job5"}.issubset(job_ids):
                            success = True
                            break
            except Exception:
                pass

        assert success, "Worker did not process all 5 jobs and submit them to the Flask API within 10 seconds."
    finally:
        worker_proc.terminate()
        worker_proc.wait(timeout=2)