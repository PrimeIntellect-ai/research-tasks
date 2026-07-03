# test_final_state.py
import os
import subprocess
import tempfile
import pytest
import numpy as np

def test_analyzer_fuzz_equivalence():
    agent_bin = "/home/user/analyzer"
    oracle_bin = "/opt/oracle/analyzer_oracle"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable"

    np.random.seed(1337)

    # Fuzz equivalence: 10 runs
    for i in range(10):
        N = np.random.randint(100, 1001)
        data = np.random.uniform(0.0, 100.0, size=N * 128).astype(np.float32)

        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(data.tobytes())
            input_path = input_file.name

        oracle_out = input_path + ".oracle.bin"
        agent_out = input_path + ".agent.bin"

        try:
            # Run oracle
            oracle_res = subprocess.run([oracle_bin, input_path, oracle_out], capture_output=True, text=True)
            assert oracle_res.returncode == 0, f"Oracle failed to run: {oracle_res.stderr}"

            # Run agent
            env = os.environ.copy()
            # Add the vendored library path to LD_LIBRARY_PATH in case rpath wasn't set
            env["LD_LIBRARY_PATH"] = "/app/fast_bootstrap-1.0:" + env.get("LD_LIBRARY_PATH", "")
            agent_res = subprocess.run([agent_bin, input_path, agent_out], capture_output=True, text=True, env=env)
            assert agent_res.returncode == 0, f"Agent binary failed to run: {agent_res.stderr}"

            assert os.path.exists(oracle_out), "Oracle did not produce an output file."
            assert os.path.exists(agent_out), "Agent did not produce an output file."

            with open(oracle_out, "rb") as f:
                oracle_data = f.read()
            with open(agent_out, "rb") as f:
                agent_data = f.read()

            if oracle_data != agent_data:
                # Convert to numpy arrays to show where it differs
                oracle_arr = np.frombuffer(oracle_data, dtype=np.float32)
                agent_arr = np.frombuffer(agent_data, dtype=np.float32)
                pytest.fail(
                    f"Output mismatch on fuzz run {i+1} (N={N}).\n"
                    f"Oracle output shape: {oracle_arr.shape}\n"
                    f"Agent output shape: {agent_arr.shape}\n"
                    f"Oracle first 10 floats: {oracle_arr[:10]}\n"
                    f"Agent first 10 floats: {agent_arr[:10]}\n"
                    "The agent's output is not bit-exactly identical to the oracle."
                )
        finally:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(oracle_out):
                os.remove(oracle_out)
            if os.path.exists(agent_out):
                os.remove(agent_out)