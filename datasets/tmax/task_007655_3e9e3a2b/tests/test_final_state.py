# test_final_state.py
import os
import re

def test_modern_project_exists():
    assert os.path.isdir('/home/user/modern_project'), "Modern project directory is missing"

def test_venv_exists():
    assert os.path.isdir('/home/user/modern_project/venv'), "Virtual environment directory 'venv' is missing"
    assert os.path.isfile('/home/user/modern_project/venv/bin/python') or os.path.isfile('/home/user/modern_project/venv/bin/python3'), "Python executable not found in venv"

def test_requirements_file():
    req_path = '/home/user/modern_project/requirements.txt'
    assert os.path.isfile(req_path), "requirements.txt is missing in modern project"
    with open(req_path, 'r') as f:
        content = f.read()
    assert re.search(r'Flask\s*>=\s*2\.0\.0', content, re.IGNORECASE), "Flask>=2.0.0 not found in requirements.txt"
    assert re.search(r'Werkzeug\s*>=\s*2\.0\.0', content, re.IGNORECASE), "Werkzeug>=2.0.0 not found in requirements.txt"

def test_app_py_migrated():
    app_path = '/home/user/modern_project/app.py'
    assert os.path.isfile(app_path), "app.py is missing in modern project"
    with open(app_path, 'r') as f:
        content = f.read()

    assert 'eval(' not in content, "Dangerous eval() call is still present in app.py"
    assert 'ast' in content, "ast module is not used in app.py"
    assert 'Exception, e:' not in content, "Legacy Python 2 exception syntax found in app.py"

def test_test_app_exists():
    assert os.path.isfile('/home/user/test_app.py'), "test_app.py script is missing"

def test_results_log():
    log_path = '/home/user/results.log'
    assert os.path.isfile(log_path), "results.log not found. Did you run test_app.py?"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in results.log, found {len(lines)}"

    assert lines[0] == "17", f"Expected first line to be '17', got '{lines[0]}'"
    assert lines[1] == "4.0", f"Expected second line to be '4.0', got '{lines[1]}'"
    assert lines[2] == "ERROR", f"Expected third line to be 'ERROR', got '{lines[2]}'"