# test_final_state.py
import os
import random
import subprocess
import pytest
import time
import urllib.request

def test_api_env_configured():
    env_path = "/app/services/api/.env"
    assert os.path.isfile(env_path), f"Missing {env_path}"
    with open(env_path, "r") as f:
        content = f.read()
    assert "REDIS_HOST=127.0.0.1" in content or "REDIS_HOST=localhost" in content, "REDIS_HOST not configured correctly in .env"

def test_libthermal_compiled():
    so_path = "/app/libthermal/libthermal.so"
    assert os.path.isfile(so_path), f"Missing compiled library {so_path}"

def test_mesh_step_executable():
    exe_path = "/app/mesh_step"
    assert os.path.isfile(exe_path), f"Missing executable {exe_path}"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable"

def test_fit_sh_executable():
    sh_path = "/app/fit.sh"
    assert os.path.isfile(sh_path), f"Missing script {sh_path}"
    assert os.access(sh_path, os.X_OK), f"{sh_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/bin/mesh_step_oracle"
    agent_path = "/app/mesh_step"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent executable missing at {agent_path}"

    # Needs libthermal.so in LD_LIBRARY_PATH
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app/libthermal:" + env.get("LD_LIBRARY_PATH", "")

    random.seed(42)
    for _ in range(100): # test 100 random inputs to keep test fast but robust
        n = random.randint(5, 100)
        temps = [random.randint(0, 10000) for _ in range(n)]
        input_str = f"{n}\n" + " ".join(map(str, temps)) + "\n"
        input_bytes = input_str.encode('utf-8')

        oracle_proc = subprocess.run([oracle_path], input=input_bytes, capture_output=True, env=env)
        agent_proc = subprocess.run([agent_path], input=input_bytes, capture_output=True, env=env)

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input {input_str}"
        assert agent_proc.stdout == oracle_proc.stdout, f"Output mismatch on input {input_str}\nOracle: {oracle_proc.stdout}\nAgent: {agent_proc.stdout}"

def test_fit_sh_execution():
    # Run fit.sh
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app/libthermal:" + env.get("LD_LIBRARY_PATH", "")

    proc = subprocess.run(["/app/fit.sh"], capture_output=True, env=env)
    assert proc.returncode == 0, f"/app/fit.sh failed with error: {proc.stderr.decode()}"

    # Check redis for final_mesh
    redis_proc = subprocess.run(["redis-cli", "get", "final_mesh"], capture_output=True, text=True)
    assert redis_proc.returncode == 0, "Failed to connect to redis"

    final_mesh = redis_proc.stdout.strip()
    assert final_mesh != "" and final_mesh != "(nil)", "final_mesh key not found in Redis"