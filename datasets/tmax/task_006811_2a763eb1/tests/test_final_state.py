# test_final_state.py
import os
import re
import subprocess

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_simulation_compiled():
    exe_path = "/home/user/sim_src/simulate"
    assert os.path.isfile(exe_path), f"Simulation executable {exe_path} was not compiled."
    assert os.access(exe_path, os.X_OK), f"Simulation executable {exe_path} is not executable."

def test_hdf5_file_generated():
    h5_path = "/home/user/sim_src/synth_data.h5"
    assert os.path.isfile(h5_path), f"HDF5 file {h5_path} was not generated."

def test_ci_output_exists():
    output_path = "/home/user/ci_output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_ci_output_format_and_values():
    output_path = "/home/user/ci_output.txt"
    assert os.path.isfile(output_path), "Output file missing."

    with open(output_path, "r") as f:
        content = f.read().strip()

    # Expected format: CI: [Lower, Upper]
    pattern = r"^CI:\s*\[(\d+\.\d{4}),\s*(\d+\.\d{4})\]$"
    match = re.match(pattern, content)
    assert match, f"Output format is incorrect. Expected 'CI: [Lower, Upper]' with 4 decimal places, got: '{content}'"

    lower_str, upper_str = match.groups()
    lower = float(lower_str)
    upper = float(upper_str)

    assert lower <= upper, "Lower bound must be less than or equal to upper bound."

    # The true mean is 18.375. The bootstrap CI bounds should be close to this.
    assert 17.5 <= lower <= 19.0, f"Lower bound {lower} is not in the expected range for the mean 18.375."
    assert 17.5 <= upper <= 19.0, f"Upper bound {upper} is not in the expected range for the mean 18.375."