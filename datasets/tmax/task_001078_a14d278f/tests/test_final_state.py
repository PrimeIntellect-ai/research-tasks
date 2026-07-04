# test_final_state.py
import os
import subprocess

BASE_DIR = "/home/user/sensor_pipeline"

def test_build_success():
    """Verify that the Makefile has been fixed and the project compiles successfully."""
    # Clean first
    subprocess.run(["make", "clean"], cwd=BASE_DIR, capture_output=True)

    # Build
    result = subprocess.run(["make"], cwd=BASE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with error:\n{result.stderr}\n{result.stdout}"

    exe_path = os.path.join(BASE_DIR, "sensor_proc")
    assert os.path.isfile(exe_path), "sensor_proc executable was not created after running make."

def test_execution_success():
    """Verify that the program runs without crashing (e.g., bypassing the segfault)."""
    exe_path = os.path.join(BASE_DIR, "sensor_proc")
    input_csv = os.path.join(BASE_DIR, "input.csv")
    output_bin = os.path.join(BASE_DIR, "output.bin")

    # Ensure the executable exists before running
    if not os.path.isfile(exe_path):
        subprocess.run(["make"], cwd=BASE_DIR, capture_output=True)

    assert os.path.isfile(exe_path), "Cannot run test: sensor_proc executable missing."

    result = subprocess.run([exe_path, input_csv, output_bin], cwd=BASE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Execution failed (possibly segfaulted on malformed line). Return code: {result.returncode}\nStderr: {result.stderr}"
    assert os.path.isfile(output_bin), "output.bin was not created by the executable."

def test_output_matches_expected():
    """Verify that the output binary exactly matches the expected binary (struct padding fixed)."""
    output_bin = os.path.join(BASE_DIR, "output.bin")
    expected_bin = os.path.join(BASE_DIR, "expected.bin")

    assert os.path.isfile(expected_bin), f"{expected_bin} is missing from the environment."
    assert os.path.isfile(output_bin), f"{output_bin} is missing. Ensure the program runs successfully."

    with open(output_bin, "rb") as f:
        output_data = f.read()

    with open(expected_bin, "rb") as f:
        expected_data = f.read()

    assert output_data == expected_data, (
        f"Output binary does not match expected binary. "
        f"Output size: {len(output_data)} bytes, Expected size: {len(expected_data)} bytes. "
        "Struct padding issue (__attribute__((packed))) or data processing logic might still be incorrect."
    )