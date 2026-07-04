# test_final_state.py
import os
import subprocess
import random
import pytest

def test_emulator_fuzz_equivalence():
    oracle = "/app/bio_sim"
    agent_script = "/home/user/emulator.py"
    agent = ["python3", agent_script]

    assert os.path.exists(agent_script), f"Agent script missing: {agent_script}"

    random.seed(42)
    for _ in range(1000):
        p0 = random.uniform(0.1, 100.0)
        r = random.uniform(0.01, 5.0)
        k = random.uniform(50.0, 500.0)
        tmax = random.uniform(1.0, 20.0)

        # Format arguments as strings
        args = [str(p0), str(r), str(k), str(tmax)]

        oracle_proc = subprocess.run([oracle] + args, capture_output=True, text=True)
        agent_proc = subprocess.run(agent + args, capture_output=True, text=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on inputs {args}"
        assert agent_proc.returncode == 0, f"Agent script failed on inputs {args}\nStderr: {agent_proc.stderr}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on inputs {args}.\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}"
        )

def test_processed_data():
    processed_file = "/home/user/processed_data.h5"
    assert os.path.exists(processed_file), f"Processed data file missing: {processed_file}"

    # We use a subprocess to run the validation script so we can safely import netCDF4 and h5py 
    # which are known to be in the environment, without violating the import allow-list of the test runner.
    check_script = """
import sys
import h5py
import netCDF4 as nc
import subprocess

try:
    ds = nc.Dataset('/home/user/raw_inputs.nc', 'r')
    P0 = ds.variables['P0'][:]
    r = ds.variables['r'][:]
    K = ds.variables['K'][:]
    Tmax = ds.variables['Tmax'][:]
    ds.close()

    with h5py.File('/home/user/processed_data.h5', 'r') as f:
        if 'final_states' not in f:
            print("Dataset 'final_states' not found in HDF5 file")
            sys.exit(1)
        final_states = f['final_states'][:]

    if len(final_states) != 50:
        print(f"Expected 50 final states, got {len(final_states)}")
        sys.exit(1)

    for i in range(50):
        args = [str(P0[i]), str(r[i]), str(K[i]), str(Tmax[i])]
        oracle_out = subprocess.run(["/app/bio_sim"] + args, capture_output=True, text=True).stdout.strip()

        expected_val = float(oracle_out)
        actual_val = float(final_states[i])

        # Check within a small tolerance due to float formatting
        if abs(expected_val - actual_val) > 1e-4:
            print(f"Mismatch at index {i} for inputs {args}: expected {expected_val}, got {actual_val}")
            sys.exit(1)

    print("OK")
except Exception as e:
    print(f"Error during validation: {str(e)}")
    sys.exit(1)
"""
    result = subprocess.run(["python3", "-c", check_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Processed data validation failed:\n{result.stdout}\n{result.stderr}"
    assert result.stdout.strip() == "OK", f"Processed data validation did not output OK:\n{result.stdout}"