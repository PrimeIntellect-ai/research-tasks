# test_final_state.py
import os
import subprocess
import time
import pandas as pd
import pytest

def test_executable_exists():
    assert os.path.isfile("/home/user/clean_data"), "Executable /home/user/clean_data not found."
    assert os.access("/home/user/clean_data", os.X_OK), "/home/user/clean_data is not executable."

def test_speedup_and_output():
    # Compile reference
    ref_c = "/app/reference_serial.c"
    ref_bin = "/tmp/ref"
    assert os.path.isfile(ref_c), f"Reference source {ref_c} missing."

    compile_cmd = ["gcc", "-O3", ref_c, "-o", ref_bin]
    subprocess.run(compile_cmd, check=True)

    # Run reference
    start_ref = time.time()
    subprocess.run([ref_bin], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time_ref = time.time() - start_ref

    # Run agent
    agent_bin = "/home/user/clean_data"
    start_agent = time.time()
    subprocess.run([agent_bin], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time_agent = time.time() - start_agent

    speedup = time_ref / time_agent if time_agent > 0 else float('inf')
    assert speedup >= 1.5, f"Speedup is {speedup:.2f}, which is less than the required 1.5 threshold. (Ref: {time_ref:.2f}s, Agent: {time_agent:.2f}s)"

def test_total_sum_accuracy():
    sum_file = "/home/user/total_sum.txt"
    assert os.path.isfile(sum_file), f"Output file {sum_file} missing."

    with open(sum_file, "r") as f:
        content = f.read().strip()

    try:
        agent_sum = float(content)
    except ValueError:
        pytest.fail(f"Could not parse {sum_file} content as float: {content}")

    csv_file = "/app/historical_transactions.csv"
    assert os.path.isfile(csv_file), f"CSV file {csv_file} missing."

    # Compute expected sum using pandas
    df = pd.read_csv(csv_file, header=None, names=["Name", "SSN", "TransactionAmount"], skipinitialspace=True)
    df_dedup = df.drop_duplicates(subset=["Name", "SSN", "TransactionAmount"])
    expected_sum = df_dedup["TransactionAmount"].sum()

    # Allow a small floating point tolerance
    assert abs(agent_sum - expected_sum) < 1.0, f"Expected sum approx {expected_sum}, but got {agent_sum}"

def test_cleaned_transactions_output():
    output_csv = "/home/user/cleaned_transactions.csv"
    assert os.path.isfile(output_csv), f"Output file {output_csv} missing."

    df = pd.read_csv(output_csv, header=None, names=["Name", "SSN", "TransactionAmount"], skipinitialspace=True)

    # Check if SSNs are masked
    ssns = df["SSN"].astype(str)
    # The first 5 digits of XXX-XX-XXXX should be ***-**-XXXX
    # So it starts with ***-**-
    unmasked = ssns[~ssns.str.match(r'^\*\*\*-\*\*-\d{4}$')]
    assert len(unmasked) == 0, f"Found {len(unmasked)} unmasked or improperly masked SSNs. Example: {unmasked.iloc[0] if len(unmasked) > 0 else ''}"