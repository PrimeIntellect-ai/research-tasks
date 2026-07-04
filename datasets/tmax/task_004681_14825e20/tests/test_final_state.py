# test_final_state.py
import os
import json
import math
import subprocess
import pytest

def get_expected_values():
    """
    Computes the expected values using a subprocess to leverage the numpy/scipy
    libraries installed by the agent, keeping this test file stdlib-only.
    """
    code = """
import numpy as np
import scipy.stats
import urllib.request
import json

url = "https://files.rcsb.org/download/1CRN.pdb"
req = urllib.request.urlopen(url)
lines = req.read().decode('utf-8').split('\\n')

coords = []
for line in lines:
    if line.startswith("ATOM") and line[12:16].strip() == "CA":
        x = float(line[30:38])
        y = float(line[38:46])
        z = float(line[46:54])
        coords.append(np.array([x, y, z]))

coords = np.array(coords)
N = len(coords)

edges = 0
degrees = np.zeros(N, dtype=int)
for i in range(N):
    for j in range(i+1, N):
        dist = np.linalg.norm(coords[i] - coords[j])
        if dist < 8.0:
            edges += 1
            degrees[i] += 1
            degrees[j] += 1

D = degrees
fft_mag = np.abs(np.fft.fft(D))
mag_positive = fft_mag[1:N//2]
peak_freq_index = int(np.argmax(mag_positive))

np.random.seed(42)
null_mags = []
for _ in range(100):
    D_shuf = np.random.permutation(D)
    null_mag = np.abs(np.fft.fft(D_shuf))[1:N//2]
    null_mags.append(null_mag)

mean_null_mag = np.mean(null_mags, axis=0)
t_stat, p_val = scipy.stats.ttest_rel(mag_positive, mean_null_mag)

print(json.dumps({
    "num_ca_atoms": N,
    "num_edges": edges,
    "peak_freq_index": peak_freq_index,
    "p_value": float(p_val)
}))
"""
    result = subprocess.run(["python3", "-c", code], capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail(f"Failed to compute expected values using agent's environment: {result.stderr}")
    return json.loads(result.stdout)

@pytest.fixture(scope="module")
def expected_data():
    return get_expected_values()

def test_script_exists():
    assert os.path.isfile("/home/user/analyze_protein.py"), "/home/user/analyze_protein.py is missing."

def test_pdb_downloaded():
    assert os.path.isfile("/home/user/1CRN.pdb"), "/home/user/1CRN.pdb is missing. The script should download it."
    assert os.path.getsize("/home/user/1CRN.pdb") > 0, "/home/user/1CRN.pdb is empty."

def test_spectrum_plot_exists():
    assert os.path.isfile("/home/user/spectrum.png"), "/home/user/spectrum.png is missing."
    assert os.path.getsize("/home/user/spectrum.png") > 0, "/home/user/spectrum.png is empty."

def test_profile_exists():
    assert os.path.isfile("/home/user/profile.txt"), "/home/user/profile.txt is missing."
    assert os.path.getsize("/home/user/profile.txt") > 0, "/home/user/profile.txt is empty. Profiling may not have executed."

def test_results_json(expected_data):
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"{results_path} is missing."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON.")

    assert "num_ca_atoms" in results, "Key 'num_ca_atoms' missing in results.json"
    assert results["num_ca_atoms"] == expected_data["num_ca_atoms"], \
        f"Expected num_ca_atoms to be {expected_data['num_ca_atoms']}, got {results['num_ca_atoms']}"

    assert "num_edges" in results, "Key 'num_edges' missing in results.json"
    assert results["num_edges"] == expected_data["num_edges"], \
        f"Expected num_edges to be {expected_data['num_edges']}, got {results['num_edges']}"

    assert "peak_freq_index" in results, "Key 'peak_freq_index' missing in results.json"
    assert results["peak_freq_index"] == expected_data["peak_freq_index"], \
        f"Expected peak_freq_index to be {expected_data['peak_freq_index']}, got {results['peak_freq_index']}"

    assert "p_value" in results, "Key 'p_value' missing in results.json"
    assert math.isclose(results["p_value"], expected_data["p_value"], abs_tol=1e-4), \
        f"Expected p_value to be close to {expected_data['p_value']}, got {results['p_value']}"