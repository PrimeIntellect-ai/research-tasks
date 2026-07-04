# test_final_state.py

import os

def test_network_gen_executable():
    """Verify that network_gen was compiled and is executable."""
    path = "/home/user/network_gen"
    assert os.path.exists(path), f"The executable {path} is missing. Did you compile network_gen.c?"
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_network_csv_exists():
    """Verify that network.csv was generated."""
    path = "/home/user/network.csv"
    assert os.path.exists(path), f"The file {path} is missing. Did you run the network generator?"
    assert os.path.isfile(path), f"{path} is not a file."

def test_model_fit_py_exists():
    """Verify that the Python script model_fit.py exists."""
    path = "/home/user/model_fit.py"
    assert os.path.exists(path), f"The script {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

def test_convergence_time_txt():
    """Verify that convergence_time.txt contains the correct convergence time."""
    path = "/home/user/convergence_time.txt"
    assert os.path.exists(path), f"The output file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "77.6", f"Expected convergence time to be '77.6', but got '{content}'."