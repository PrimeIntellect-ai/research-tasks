# test_final_state.py

import os
import math
import statistics
import subprocess

def test_minimal_crash_csv():
    minimal_crash_path = "/home/user/sim_env/minimal_crash.csv"
    assert os.path.isfile(minimal_crash_path), f"File {minimal_crash_path} is missing. You must save the minimal crashing lines here."

    with open(minimal_crash_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"minimal_crash.csv should contain exactly 2 lines, found {len(lines)}."

    val1 = float(lines[0])
    val2 = float(lines[1])

    assert math.isclose(val1, 10000000.0000001), f"First value in minimal_crash.csv is incorrect: {val1}"
    assert math.isclose(val2, 10000000.0000002), f"Second value in minimal_crash.csv is incorrect: {val2}"

def test_success_txt():
    success_path = "/home/user/sim_env/success.txt"
    assert os.path.isfile(success_path), f"File {success_path} is missing. You must save the final output here."

    # Compute the expected standard deviation
    # The variance of a dataset is invariant to shifts (adding a constant).
    # Thus, the standard deviation of the final positions is the same as the initial positions.
    initial_data = [
        10.1, 10.2, 10.3, 10.15, 10.25, 
        10000000.0000001, 10000000.0000002, 
        10.4, 10.5, 10.6
    ]
    expected_std_dev = statistics.stdev(initial_data)

    with open(success_path, 'r') as f:
        content = f.read().strip()

    assert content, "success.txt is empty."

    try:
        actual_std_dev = float(content)
    except ValueError:
        pytest.fail(f"success.txt does not contain a valid float: {content}")

    assert math.isclose(actual_std_dev, expected_std_dev, rel_tol=1e-5), \
        f"Standard deviation in success.txt is incorrect. Expected ~{expected_std_dev}, got {actual_std_dev}"

def test_sim_py_fixes():
    sim_py_path = "/home/user/sim_env/sim.py"
    inputs_csv_path = "/home/user/sim_env/inputs.csv"

    assert os.path.isfile(sim_py_path), f"File {sim_py_path} is missing."

    # Run the simulation script to ensure it doesn't crash (recursion or ValueError)
    result = subprocess.run(
        ["python3", sim_py_path, inputs_csv_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, \
        f"sim.py failed to run. Return code: {result.returncode}\nStderr: {result.stderr}"

    output = result.stdout.strip()
    try:
        actual_std_dev = float(output)
    except ValueError:
        pytest.fail(f"Output of sim.py is not a valid float: {output}")

    initial_data = [
        10.1, 10.2, 10.3, 10.15, 10.25, 
        10000000.0000001, 10000000.0000002, 
        10.4, 10.5, 10.6
    ]
    expected_std_dev = statistics.stdev(initial_data)

    assert math.isclose(actual_std_dev, expected_std_dev, rel_tol=1e-5), \
        f"Output of sim.py is incorrect. Expected ~{expected_std_dev}, got {actual_std_dev}"