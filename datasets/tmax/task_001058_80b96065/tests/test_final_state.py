# test_final_state.py

import os
import ctypes
import math
import subprocess
import tempfile
import pytest
import requests
import numpy as np
from scipy.optimize import fsolve

def get_expected_values():
    c_src = "/app/src/mc_sampler.c"
    assert os.path.isfile(c_src), "C source file missing at /app/src/mc_sampler.c"

    with tempfile.TemporaryDirectory() as tmpdir:
        so_path = os.path.join(tmpdir, "sampler.so")
        subprocess.run(["gcc", "-shared", "-o", so_path, "-fPIC", c_src, "-lm"], check=True)

        lib = ctypes.CDLL(so_path)
        lib.generate_samples.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        lib.generate_samples.restype = None

        seed = 42
        n = 1000000
        out_array = (ctypes.c_double * n)()
        lib.generate_samples(seed, n, out_array)

        samples = np.ctypeslib.as_array(out_array)

        energy = math.fsum(samples**2)
        f_avg = math.fsum(samples) / n

        def equation(x):
            return 1.2 * x**3 + 0.8 * x - f_avg

        displacement = fsolve(equation, 0.0)[0]

        return energy, displacement

def test_api_simulate():
    expected_energy, expected_displacement = get_expected_values()

    url = "http://127.0.0.1:8080/simulate"
    headers = {
        "Authorization": "Bearer sim_token_xyz",
        "Content-Type": "application/json"
    }
    payload = {
        "seed": 42,
        "num_samples": 1000000
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Failed to parse JSON response. Response body: {response.text}")

    assert "energy" in data, f"Response JSON missing 'energy'. Got: {data}"
    assert "displacement" in data, f"Response JSON missing 'displacement'. Got: {data}"

    assert math.isclose(data["energy"], expected_energy, rel_tol=1e-9), f"Energy mismatch: expected {expected_energy}, got {data['energy']}"
    assert math.isclose(data["displacement"], expected_displacement, rel_tol=1e-7), f"Displacement mismatch: expected {expected_displacement}, got {data['displacement']}"

def test_api_auth_required():
    url = "http://127.0.0.1:8080/simulate"
    payload = {
        "seed": 42,
        "num_samples": 1000000
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {response.status_code}. Response body: {response.text}"