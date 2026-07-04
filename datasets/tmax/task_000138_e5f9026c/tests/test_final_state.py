# test_final_state.py

import os
import stat

def test_clean_spectra_csv():
    """Test that clean_spectra.csv exists and contains the correctly filtered data."""
    csv_path = "/home/user/clean_spectra.csv"
    assert os.path.exists(csv_path), f"File {csv_path} is missing."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    expected_lines = [
        "498.0,1.2",
        "499.0,2.1",
        "499.5,5.4",
        "500.0,10.2",
        "500.5,8.1",
        "501.0,3.2",
        "501.5,1.5",
        "502.5,1.1"
    ]

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {csv_path}, but found {len(lines)}."

    for expected, actual in zip(expected_lines, lines):
        assert expected == actual, f"Expected line '{expected}', but found '{actual}'."

def test_fitter_executable():
    """Test that the Go program was compiled to /home/user/fitter and is executable."""
    exe_path = "/home/user/fitter"
    assert os.path.exists(exe_path), f"Executable {exe_path} is missing."
    assert os.path.isfile(exe_path), f"{exe_path} is not a file."

    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {exe_path} is not executable."

def test_final_parameters_log():
    """Test that final_parameters.log exists and contains the correct MCMC estimates."""
    log_path = "/home/user/final_parameters.log"
    assert os.path.exists(log_path), f"File {log_path} is missing."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    expected_content = {
        "Amplitude": "16.40",
        "Center": "500.25",
        "Width": "1.25",
        "Background": "1.05"
    }

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in {log_path}, but found {len(lines)}."

    parsed_params = {}
    for line in lines:
        parts = line.split(":")
        assert len(parts) == 2, f"Line '{line}' does not match the format 'Parameter: <value>'."
        key = parts[0].strip()
        val = parts[1].strip()
        parsed_params[key] = val

    for key, expected_val in expected_content.items():
        assert key in parsed_params, f"Missing parameter '{key}' in {log_path}."
        assert parsed_params[key] == expected_val, f"Expected {key} to be {expected_val}, but found {parsed_params[key]}."