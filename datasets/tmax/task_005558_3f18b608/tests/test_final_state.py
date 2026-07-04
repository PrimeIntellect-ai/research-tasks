# test_final_state.py
import os
import pytest

def test_mcmc_cpp_fixed():
    mcmc_file = "/home/user/mcmc_project/mcmc.cpp"
    assert os.path.isfile(mcmc_file), f"{mcmc_file} is missing."
    with open(mcmc_file, "r") as f:
        content = f.read()

    # Check if there is some logic to cap dt
    assert "dt =" in content or "dt=" in content, "No dt assignment found in mcmc.cpp."
    assert "t_end - t" in content or "t_end-t" in content, "The logic to cap dt to (t_end - t) is missing in mcmc.cpp."

def test_executable_exists():
    assert os.path.isfile("/home/user/mcmc_project/mcmc_sim"), "The compiled executable mcmc_sim is missing."
    assert os.access("/home/user/mcmc_project/mcmc_sim", os.X_OK), "mcmc_sim is not executable."

def test_posterior_txt_exists():
    posterior_file = "/home/user/mcmc_project/posterior.txt"
    assert os.path.isfile(posterior_file), f"{posterior_file} is missing."
    with open(posterior_file, "r") as f:
        lines = f.readlines()
    assert len(lines) > 0, "posterior.txt is empty."

def test_wasserstein_distance_file():
    distance_file = "/home/user/mcmc_project/wasserstein_distance.txt"
    assert os.path.isfile(distance_file), f"{distance_file} is missing."
    with open(distance_file, "r") as f:
        content = f.read().strip()

    try:
        distance = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {distance_file} as a float. Content: '{content}'")

    assert 0.0 <= distance < 0.15, f"Wasserstein distance {distance} is out of expected bounds [0.0, 0.15). The bug might not be properly fixed."