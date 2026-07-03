# test_final_state.py

import os
import subprocess
import py_compile

def test_dfa_models_dir():
    assert os.path.isdir("/home/user/dfa_models"), "/home/user/dfa_models/ directory is missing."
    assert os.path.isfile("/home/user/dfa_models/m1.dfa"), "m1.dfa is missing from /home/user/dfa_models/."
    assert os.path.isfile("/home/user/dfa_models/m2.dfa"), "m2.dfa is missing from /home/user/dfa_models/."

def test_m2_dfa_patched():
    m2_path = "/home/user/dfa_models/m2.dfa"
    assert os.path.isfile(m2_path), f"{m2_path} is missing."
    with open(m2_path, "r") as f:
        content = f.read()
    assert "q2, 1 -> q2" in content, "m2.dfa does not contain the patched transition 'q2, 1 -> q2'."
    assert "q2, 1 -> q0" not in content, "m2.dfa still contains the buggy transition 'q2, 1 -> q0'."

def test_simulator_exists_and_valid():
    sim_path = "/home/user/simulator.py"
    assert os.path.isfile(sim_path), f"{sim_path} is missing."
    try:
        py_compile.compile(sim_path, doraise=True)
    except Exception as e:
        assert False, f"simulator.py contains invalid Python code: {e}"

def test_test_simulator_passes():
    test_path = "/home/user/test_simulator.py"
    assert os.path.isfile(test_path), f"{test_path} is missing."

    with open(test_path, "r") as f:
        content = f.read()
    assert "unittest" in content, "test_simulator.py does not seem to use the 'unittest' framework."

    # Run the tests
    result = subprocess.run(["python3", "-m", "unittest", test_path], capture_output=True, text=True)
    assert result.returncode == 0, f"test_simulator.py failed to run successfully.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_evaluation_log():
    log_path = "/home/user/evaluation.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "m1.dfa: REJECT\nm2.dfa: ACCEPT"
    assert content == expected_content, f"evaluation.log content is incorrect. Expected:\n{expected_content}\nGot:\n{content}"