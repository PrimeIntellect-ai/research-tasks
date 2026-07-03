# test_final_state.py
import os
import subprocess
import pytest

def test_ci_txt_exists():
    assert os.path.isfile("/home/user/pipeline/ci.txt"), "/home/user/pipeline/ci.txt is missing"

def test_mc_det_cpp_fixed():
    assert os.path.isfile("/home/user/pipeline/mc_det.cpp"), "/home/user/pipeline/mc_det.cpp is missing"
    with open("/home/user/pipeline/mc_det.cpp", "r") as f:
        content = f.read()

    assert "double" in content, "mc_det.cpp does not seem to be updated to use double precision."
    assert "float" not in content, "mc_det.cpp still contains 'float' types; it should be completely updated to 'double'."

def test_ci_txt_content():
    # Compile a reference C++ program to compute the exact expected output
    # This guarantees we match the environment's rand() deterministic behavior.
    ref_cpp = """#include <iostream>
#include <vector>
#include <cstdlib>
#include <iomanip>
#include <string>

using namespace std;

int main(int argc, char** argv) {
    double m[9];
    for (int i = 0; i < 9; ++i) {
        m[i] = stod(argv[i+1]);
    }

    srand(42);
    for (int iter = 0; iter < 1000; ++iter) {
        double m_pert[9];
        for (int i = 0; i < 9; ++i) {
            double noise = (rand() % 2001 - 1000) * 1e-9;
            m_pert[i] = m[i] + noise;
        }

        double det = m_pert[0] * (m_pert[4] * m_pert[8] - m_pert[5] * m_pert[7])
                   - m_pert[1] * (m_pert[3] * m_pert[8] - m_pert[5] * m_pert[6])
                   + m_pert[2] * (m_pert[3] * m_pert[7] - m_pert[4] * m_pert[6]);

        cout << fixed << setprecision(10) << det << "\\n";
    }
    return 0;
}
"""
    ref_cpp_path = "/tmp/ref_solve.cpp"
    ref_exe_path = "/tmp/ref_solve"

    with open(ref_cpp_path, "w") as f:
        f.write(ref_cpp)

    # Compile the reference program
    compile_proc = subprocess.run(["g++", ref_cpp_path, "-o", ref_exe_path], capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Failed to compile reference C++ code:\n{compile_proc.stderr}"

    # Run the reference program with the known matrix values from the HDF5 file
    args = [ref_exe_path, "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.000001"]
    run_proc = subprocess.run(args, capture_output=True, text=True)
    assert run_proc.returncode == 0, f"Failed to run reference C++ code:\n{run_proc.stderr}"

    # Parse and sort the outputs numerically
    outputs = run_proc.stdout.strip().split('\n')
    assert len(outputs) == 1000, "Reference program did not output exactly 1000 lines."

    # Sort numerically (equivalent to `sort -n`)
    outputs.sort(key=float)

    # 25th value (index 24) and 975th value (index 974)
    expected_lower = outputs[24]
    expected_upper = outputs[974]

    expected_ci = f"{expected_lower},{expected_upper}"

    # Check the student's output
    with open("/home/user/pipeline/ci.txt", "r") as f:
        actual_ci = f.read().strip()

    assert actual_ci == expected_ci, f"The contents of ci.txt ({actual_ci}) do not match the expected confidence interval ({expected_ci}). Check the percentiles and sorting."