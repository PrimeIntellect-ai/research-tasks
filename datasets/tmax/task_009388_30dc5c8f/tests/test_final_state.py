# test_final_state.py
import os
import subprocess

def test_match_s_extracted():
    assert os.path.isfile('/home/user/waf_util/match.s'), "match.s was not extracted from deps.tar.gz"

def test_makefile_fixed():
    makefile_path = '/home/user/waf_util/Makefile'
    assert os.path.isfile(makefile_path), "Makefile is missing"
    with open(makefile_path, 'r') as f:
        lines = f.readlines()

    # Check if there are recipe lines starting with a tab
    has_tabs = any(line.startswith('\t') for line in lines)
    assert has_tabs, "Makefile does not contain tab indentation for rules. Spaces were not replaced with tabs."

def test_waf_out_built_and_executable():
    waf_out_path = '/home/user/waf_util/waf.out'
    assert os.path.isfile(waf_out_path), "waf.out was not built"
    assert os.access(waf_out_path, os.X_OK), "waf.out is not executable"

def test_test_sh_exists():
    assert os.path.isfile('/home/user/waf_util/test.sh'), "test.sh script is missing"

def test_test_results_log():
    log_path = '/home/user/waf_util/test_results.log'
    assert os.path.isfile(log_path), "test_results.log is missing"

    with open(log_path, 'r') as f:
        content = f.read()

    expected_content = "Status: 200 OK\n\nStatus: 403 Forbidden\n\n"
    assert content == expected_content, f"test_results.log content is incorrect. Expected exactly:\n{repr(expected_content)}\nGot:\n{repr(content)}"

def test_waf_out_behavior():
    waf_out_path = '/home/user/waf_util/waf.out'
    if not os.path.isfile(waf_out_path):
        return # Handled by another test

    # Test valid query string
    env1 = os.environ.copy()
    env1['QUERY_STRING'] = 'id=123'
    proc1 = subprocess.run([waf_out_path], env=env1, capture_output=True, text=True)
    assert proc1.stdout == "Status: 200 OK\n\n", "waf.out did not print the correct 200 OK status for a valid QUERY_STRING"

    # Test path traversal query string
    env2 = os.environ.copy()
    env2['QUERY_STRING'] = 'file=../../etc/passwd'
    proc2 = subprocess.run([waf_out_path], env=env2, capture_output=True, text=True)
    assert proc2.stdout == "Status: 403 Forbidden\n\n", "waf.out did not print the correct 403 Forbidden status for a traversal QUERY_STRING"

    # Test missing query string
    env3 = os.environ.copy()
    if 'QUERY_STRING' in env3:
        del env3['QUERY_STRING']
    proc3 = subprocess.run([waf_out_path], env=env3, capture_output=True, text=True)
    assert proc3.stdout == "Status: 400 Bad Request\n\n", "waf.out did not print the correct 400 Bad Request status when QUERY_STRING is unset"