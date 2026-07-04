# test_final_state.py
import os
import pstats

def test_libalign_so_exists():
    path = "/home/user/libalign.so"
    assert os.path.exists(path), f"Shared library {path} does not exist. Did you compile the C file?"

def test_profile_script_exists():
    path = "/home/user/profile_pcr.py"
    assert os.path.exists(path), f"Python script {path} does not exist."

def test_ode_profile_exists_and_valid():
    path = "/home/user/ode_profile.prof"
    assert os.path.exists(path), f"Profile stats file {path} does not exist."

    # Check if it's a valid cProfile stats file
    try:
        stats = pstats.Stats(path)
        assert len(stats.stats) > 0, "Profile stats file is empty or invalid."
    except Exception as e:
        assert False, f"Failed to parse profile stats file {path}: {e}"

def test_result_txt():
    path = "/home/user/result.txt"
    assert os.path.exists(path), f"Result file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "749.00", f"Expected result.txt to contain '749.00', but got '{content}'"