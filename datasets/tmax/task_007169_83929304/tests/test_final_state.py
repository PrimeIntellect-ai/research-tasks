# test_final_state.py

import os
import math

def test_project_directory_exists():
    assert os.path.isdir("/home/user/fitter_project"), "Directory /home/user/fitter_project does not exist."

def test_cmake_lists_exists():
    assert os.path.isfile("/home/user/fitter_project/CMakeLists.txt"), "CMakeLists.txt is missing in /home/user/fitter_project."

def test_cpp_source_exists():
    files = os.listdir("/home/user/fitter_project")
    cpp_files = [f for f in files if f.endswith(".cpp") or f.endswith(".cc") or f.endswith(".cxx")]
    assert len(cpp_files) > 0, "No C++ source files found in /home/user/fitter_project."

def test_executable_exists():
    # Executable could be in the project dir or a build subdirectory
    found = False
    for root, dirs, files in os.walk("/home/user/fitter_project"):
        if "model_fitter" in files:
            found = True
            break
    assert found, "Executable 'model_fitter' not found in /home/user/fitter_project or its subdirectories."

def test_kl_result():
    result_file = "/home/user/kl_result.txt"
    assert os.path.isfile(result_file), f"The result file {result_file} is missing."

    with open(result_file, "r") as f:
        content = f.read().strip()

    # Recompute the expected value to be principled
    # 1. Root finding for x * exp(x) = 15
    # Newton-Raphson
    lam = 2.0
    for _ in range(20):
        f_val = lam * math.exp(lam) - 15
        f_prime = math.exp(lam) + lam * math.exp(lam)
        lam = lam - f_val / f_prime

    # 2. Compute Q
    P = [0.10, 0.30, 0.40, 0.15, 0.05]
    Q_unnorm = [math.exp(-lam) * (lam**k) / math.factorial(k) for k in range(5)]
    S = sum(Q_unnorm)
    Q = [q / S for q in Q_unnorm]

    # 3. Compute KL Divergence
    kl = sum(P[k] * math.log(P[k] / Q[k]) for k in range(5))
    expected_output = f"{kl:.6f}"

    assert content == expected_output, f"Expected KL divergence {expected_output}, but got {content}."