# test_final_state.py

import os
import stat
import subprocess
import tempfile
import numpy as np
import pytest

def test_shared_library_exists():
    lib_path = "/app/libspecfact-1.2.0/libspecfact.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not built."

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.py"
    assert os.path.isfile(script_path), f"Pipeline script {script_path} does not exist."
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"Pipeline script {script_path} is not executable."

def test_fuzz_equivalence():
    script_path = "/home/user/pipeline.py"
    oracle_path = "/app/oracle/reference_pipeline"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} not found."

    np.random.seed(42)
    N = 50

    for i in range(N):
        # Generate random input
        input_data = np.random.uniform(0.0, 1.0, 65536).astype(np.float64)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f_in:
            f_in.write(input_data.tobytes())
            input_file = f_in.name

        agent_out = input_file + "_agent.bin"
        oracle_out = input_file + "_oracle.bin"

        try:
            # Run oracle
            subprocess.run([oracle_path, input_file, oracle_out], check=True, capture_output=True)

            # Run agent
            subprocess.run([script_path, input_file, agent_out], check=True, capture_output=True)

            # Compare outputs
            assert os.path.isfile(agent_out), f"Agent did not produce output file {agent_out}"
            assert os.path.isfile(oracle_out), f"Oracle did not produce output file {oracle_out}"

            with open(agent_out, 'rb') as f:
                agent_bytes = f.read()
            with open(oracle_out, 'rb') as f:
                oracle_bytes = f.read()

            assert len(agent_bytes) == 1024, f"Expected agent output to be 1024 bytes, got {len(agent_bytes)}"
            assert agent_bytes == oracle_bytes, f"Fuzz mismatch on iteration {i}: agent output does not match oracle output."

        finally:
            for f in [input_file, agent_out, oracle_out]:
                if os.path.exists(f):
                    os.remove(f)

def test_visualization_generated():
    plot_path = "/home/user/visualization.png"
    assert os.path.isfile(plot_path), f"Visualization plot {plot_path} was not generated."