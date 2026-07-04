# test_final_state.py
import os
import pytest

def test_pipeline_scripts_exist():
    """Ensure that the required scripts and environment were created."""
    assert os.path.isdir("/home/user/perf_env"), "Virtual environment /home/user/perf_env is missing."
    assert os.path.isfile("/home/user/extract_signal.sh"), "Script /home/user/extract_signal.sh is missing."
    assert os.path.isfile("/home/user/fft_analyzer.py"), "Script /home/user/fft_analyzer.py is missing."
    assert os.path.isfile("/home/user/run_pipeline.sh"), "Script /home/user/run_pipeline.sh is missing."

def test_dominant_frequency_output():
    """Check that the output file contains the correct dominant frequency within the allowed tolerance."""
    output_file = "/home/user/dominant_frequency.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} not found."

    with open(output_file, "r") as f:
        content = f.read().strip()

    try:
        agent_freq = float(content)
    except ValueError:
        pytest.fail(f"Output in {output_file} is not a valid float. Got: '{content}'")

    target_freq = 12.0
    tolerance = 0.5
    error = abs(agent_freq - target_freq)

    assert error <= tolerance, (
        f"Failure: Agent frequency {agent_freq} is outside {tolerance} of "
        f"target {target_freq} (error: {error})."
    )