# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/matheval"

def test_cmakelists_fixed():
    """Check if CMakeLists.txt was fixed to link the correct library."""
    cmake_path = os.path.join(BASE_DIR, "CMakeLists.txt")
    assert os.path.isfile(cmake_path), f"{cmake_path} is missing."

    with open(cmake_path, "r") as f:
        content = f.read()

    assert "matheval_lib" not in content, "CMakeLists.txt still contains the incorrect 'matheval_lib' link target."
    assert "target_link_libraries(test_eval matheval)" in content.replace(" ", "") or \
           "target_link_libraries(test_evalmatheval)" in content.replace(" ", ""), \
           "CMakeLists.txt must link test_eval to matheval."

def test_eval_c_fixed():
    """Check if eval.c logic bugs for subtraction and division are fixed."""
    eval_c_path = os.path.join(BASE_DIR, "src", "eval.c")
    assert os.path.isfile(eval_c_path), f"{eval_c_path} is missing."

    with open(eval_c_path, "r") as f:
        content = f.read()

    assert "val1 - val2" not in content, "eval.c still contains the subtraction bug (val1 - val2)."
    assert "val1 / val2" not in content, "eval.c still contains the division bug (val1 / val2)."

    # Check for correct logic
    assert "val2 - val1" in content, "eval.c should subtract val1 from val2."
    assert "val2 / val1" in content, "eval.c should divide val2 by val1."

def test_build_and_ctest_pass():
    """Check if the project builds and tests pass."""
    build_dir = os.path.join(BASE_DIR, "build")
    assert os.path.isdir(build_dir), f"{build_dir} is missing."

    # Run cmake
    cmake_proc = subprocess.run(["cmake", ".."], cwd=build_dir, capture_output=True, text=True)
    assert cmake_proc.returncode == 0, f"CMake configuration failed:\n{cmake_proc.stderr}"

    # Run make
    make_proc = subprocess.run(["make"], cwd=build_dir, capture_output=True, text=True)
    assert make_proc.returncode == 0, f"Make build failed:\n{make_proc.stderr}"

    # Run ctest
    # Note: RPATH issues might cause ctest to fail if LD_LIBRARY_PATH isn't set or RPATH isn't fixed
    # We will just run ctest. The student was supposed to fix the RPATH issue or set env vars in python, 
    # but the instructions say "Ensure ctest can execute successfully."
    ctest_proc = subprocess.run(["ctest", "--output-on-failure"], cwd=build_dir, capture_output=True, text=True)
    assert ctest_proc.returncode == 0, f"ctest failed. Tests did not pass or executable could not find shared library:\n{ctest_proc.stderr}\n{ctest_proc.stdout}"

def test_integration_result_log():
    """Check if the integration test produced the correct result log."""
    log_path = os.path.join(BASE_DIR, "integration_result.log")
    assert os.path.isfile(log_path), f"{log_path} is missing. The integration test may not have run or failed to create the file."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "5.0" in content, f"Expected the result log to contain '5.0', but got: '{content}'"