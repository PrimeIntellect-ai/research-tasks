# test_final_state.py

import os
import stat
import subprocess
import ast

def test_package_sh_exists_and_executable():
    path = "/home/user/package.sh"
    assert os.path.isfile(path), f"{path} is missing"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable"

def test_parser_refactored():
    parser_path = "/home/user/log_processor/parser.py"
    assert os.path.isfile(parser_path), f"{parser_path} is missing"

    with open(parser_path, "r") as f:
        source = f.read()

    tree = ast.parse(source)

    # Check for LogParser class
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    assert "LogParser" in classes, "LogParser class not found in parser.py"

    # Check that CURRENT_STATE and PARSED_DATA are not in the module level assignments
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assert target.id not in ("CURRENT_STATE", "PARSED_DATA"), f"Global variable {target.id} found in parser.py"

def test_package_sh_execution():
    path = "/home/user/package.sh"
    # Run the script
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"{path} failed with output:\n{result.stdout}\n{result.stderr}"

def test_venv_and_pytest_installed():
    pytest_path = "/home/user/venv/bin/pytest"
    assert os.path.isfile(pytest_path), f"{pytest_path} is missing. Did the script install pytest in the venv?"

def test_tarball_created():
    tarball_path = "/home/user/log_processor.tar.gz"
    assert os.path.isfile(tarball_path), f"{tarball_path} is missing. Did the script create the tarball?"

def test_test_files_updated():
    test_start_path = "/home/user/log_processor/tests/test_start.py"
    test_stop_path = "/home/user/log_processor/tests/test_stop.py"

    with open(test_start_path, "r") as f:
        start_content = f.read()
    assert "LogParser" in start_content, "LogParser not used in test_start.py"

    with open(test_stop_path, "r") as f:
        stop_content = f.read()
    assert "LogParser" in stop_content, "LogParser not used in test_stop.py"