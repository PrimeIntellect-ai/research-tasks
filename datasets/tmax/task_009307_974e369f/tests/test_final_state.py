# test_final_state.py
import os
import stat
import pytest

def test_audit_script_exists_and_executable():
    script_path = '/home/user/audit_graph.sh'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable."

def test_dangling_edges_csv():
    output_path = '/home/user/dangling_edges.csv'
    assert os.path.isfile(output_path), f"The file {output_path} does not exist."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "99,MANAGES,3",
        "4,HOSTS,88"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected dangling edge '{expected}' not found in {output_path}."

    assert len(lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} dangling edges, but found {len(lines)}."

def test_vulnerable_dbs_csv():
    output_path = '/home/user/vulnerable_dbs.csv'
    assert os.path.isfile(output_path), f"The file {output_path} does not exist."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Bob,ClusterBeta,DB_Users",
        "Charlie,ClusterGamma,DB_Logs"
    ]

    assert lines == expected_lines, f"The contents of {output_path} do not match the expected output or are not sorted correctly. Expected: {expected_lines}, Got: {lines}"