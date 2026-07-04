# test_final_state.py
import os
import subprocess
import random

def test_libfastcsv_built():
    """Verify that the static library was successfully built."""
    lib_path = "/app/fastcsv-1.0/libfastcsv.a"
    assert os.path.isfile(lib_path), f"The static library {lib_path} does not exist. Did you fix the Makefile and run make?"

def test_agent_executable_exists():
    """Verify that the agent's executable exists and is executable."""
    exe_path = "/home/user/process"
    assert os.path.isfile(exe_path), f"The executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def generate_fuzz_input() -> str:
    """Generate a random CSV input according to the specification."""
    num_rows = random.randint(10, 500)
    groups = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]

    lines = ["id,group,feature_x,feature_y"]
    for _ in range(num_rows):
        id_val = random.randint(1, 10000)
        group = random.choice(groups)
        feature_x = random.uniform(-1000.0, 1000.0)
        feature_y = random.uniform(-1000.0, 1000.0)
        # Format to ensure precision doesn't cause parsing issues, though standard floats are fine
        lines.append(f"{id_val},{group},{feature_x:.6f},{feature_y:.6f}")

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    """Fuzz-test the agent's executable against the oracle."""
    oracle_path = "/app/oracle_process"
    agent_path = "/home/user/process"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} missing."
    assert os.access(oracle_path, os.X_OK), f"Oracle {oracle_path} not executable."

    random.seed(42)
    N = 100

    for i in range(N):
        csv_input = generate_fuzz_input()

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=csv_input,
            text=True,
            capture_output=True,
            check=False
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i} with error:\n{oracle_proc.stderr}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=csv_input,
            text=True,
            capture_output=True,
            check=False
        )
        assert agent_proc.returncode == 0, f"Your program failed on iteration {i} with error:\n{agent_proc.stderr}"
        agent_output = agent_proc.stdout

        # Compare
        if oracle_output != agent_output:
            error_msg = (
                f"Output mismatch on iteration {i}.\n\n"
                f"--- INPUT CSV (first 5 lines) ---\n"
                f"{chr(10).join(csv_input.splitlines()[:5])}\n"
                f"...\n\n"
                f"--- EXPECTED OUTPUT (Oracle) ---\n"
                f"{oracle_output}\n"
                f"--- ACTUAL OUTPUT (Your program) ---\n"
                f"{agent_output}\n"
            )
            assert False, error_msg