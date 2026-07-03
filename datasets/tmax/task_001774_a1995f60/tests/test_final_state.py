# test_final_state.py
import os
import csv
import json
import math
import pytest

WORKSPACE_DIR = "/home/user/workspace"

def get_expected_values():
    csv_path = os.path.join(WORKSPACE_DIR, "spectrum.csv")
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            data.append((float(row['Wavenumber']), float(row['Intensity'])))

    smoothed = []
    for i in range(len(data)):
        if i < 2 or i > len(data) - 3:
            smoothed.append(None)
        else:
            avg = sum(data[j][1] for j in range(i-2, i+3)) / 5.0
            smoothed.append(avg)

    peaks = []
    for i in range(2, len(data) - 2):
        val = smoothed[i]
        if (val > smoothed[i-1] and val > smoothed[i-2] and 
            val > smoothed[i+1] and val > smoothed[i+2]):
            peaks.append((val, data[i][0]))

    peaks.sort(reverse=True)
    exp_peaks = sorted([p[1] for p in peaks[:3]])

    # Theoretical peaks derived from the graph structure in molecule.edges
    # Unique degrees: 1, 3, 5, 6
    # Top 3 degrees: 6, 5, 3
    # Peaks: 6*314.15, 5*314.15, 3*314.15
    theo_peaks = sorted([6 * 314.15, 5 * 314.15, 3 * 314.15])

    mse = sum((t - e)**2 for t, e in zip(theo_peaks, exp_peaks)) / 3.0
    return theo_peaks, exp_peaks, mse

def test_calc_peaks_executable_exists():
    exe_path = os.path.join(WORKSPACE_DIR, "calc_peaks")
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing. Did you compile the C program?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_results_json():
    json_path = os.path.join(WORKSPACE_DIR, "results.json")
    assert os.path.isfile(json_path), f"JSON file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "theoretical_peaks" in results, "Key 'theoretical_peaks' missing from results.json"
    assert "experimental_peaks" in results, "Key 'experimental_peaks' missing from results.json"
    assert "mse" in results, "Key 'mse' missing from results.json"

    expected_theo, expected_exp, expected_mse = get_expected_values()

    # Check theoretical peaks
    actual_theo = results["theoretical_peaks"]
    assert len(actual_theo) == 3, "Expected exactly 3 theoretical peaks."
    for a, e in zip(actual_theo, expected_theo):
        assert math.isclose(a, e, rel_tol=1e-3, abs_tol=1e-2), f"Theoretical peak {a} does not match expected {e}."

    # Check experimental peaks
    actual_exp = results["experimental_peaks"]
    assert len(actual_exp) == 3, "Expected exactly 3 experimental peaks."
    for a, e in zip(actual_exp, expected_exp):
        assert math.isclose(a, e, rel_tol=1e-3, abs_tol=1e-2), f"Experimental peak {a} does not match expected {e}."

    # Check MSE
    actual_mse = results["mse"]
    assert math.isclose(actual_mse, expected_mse, rel_tol=1e-3, abs_tol=1e-2), f"MSE {actual_mse} does not match expected {expected_mse}."

def test_spectrum_plot_exists():
    plot_path = os.path.join(WORKSPACE_DIR, "spectrum_plot.png")
    assert os.path.isfile(plot_path), f"Plot file {plot_path} is missing."
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty."