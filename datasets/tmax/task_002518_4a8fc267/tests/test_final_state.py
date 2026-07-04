# test_final_state.py
import os
import re

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_value = str(int(8000 * 8000 * 0.5 * 10))
    assert expected_value in content, f"Expected value {expected_value} not found in {report_path}."

def test_executable_exists():
    exe_path = "/home/user/mc_sim"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_mc_sim_cpp_fixed():
    cpp_path = "/home/user/mc_sim.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    # Extract the calculate_energy function body
    match = re.search(r'double\s+calculate_energy\s*\(\)\s*\{(.+?)return\s+sum;', content, re.DOTALL)
    assert match, "Could not find the calculate_energy function body."

    func_body = match.group(1)

    # Find the order of loops
    i_pos = func_body.find('for (int i')
    if i_pos == -1:
        i_pos = func_body.find('for(int i')

    j_pos = func_body.find('for (int j')
    if j_pos == -1:
        j_pos = func_body.find('for(int j')

    assert i_pos != -1 and j_pos != -1, "Could not find both 'i' and 'j' loops in calculate_energy."

    # In row-major traversal for data[i][j], the outer loop should be 'i' and inner loop should be 'j'.
    # Or if access is data[j][i], outer is 'j' and inner is 'i'.
    # Let's check the access pattern.
    access_ij = func_body.find('data[i][j]') != -1
    access_ji = func_body.find('data[j][i]') != -1

    assert access_ij or access_ji, "Could not find array access data[i][j] or data[j][i]."

    if access_ij:
        assert i_pos < j_pos, "Loop 'i' should be the outer loop (appear before loop 'j') for data[i][j] access."
    if access_ji:
        assert j_pos < i_pos, "Loop 'j' should be the outer loop (appear before loop 'i') for data[j][i] access."