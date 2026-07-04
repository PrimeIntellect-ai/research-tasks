# test_final_state.py
import os

def test_parser_c_exists():
    assert os.path.isfile("/home/user/parser.c"), "/home/user/parser.c is missing"

def test_parser_executable_exists():
    assert os.path.isfile("/home/user/parser"), "/home/user/parser executable is missing"
    assert os.access("/home/user/parser", os.X_OK), "/home/user/parser is not executable"

def test_organize_sh_exists():
    assert os.path.isfile("/home/user/organize.sh"), "/home/user/organize.sh is missing"

def test_project_log_contents():
    log_path = "/home/user/project_log.txt"
    assert os.path.isfile(log_path), f"{log_path} is missing"

    expected_lines = {
        "[1630000000] System initialized.",
        "[1630000005] Module A loaded.",
        "[1630000010] Warning: low memory.",
        "[1630000020] User logged in.",
        "[1630000025] Data sync complete."
    }

    with open(log_path, "r") as f:
        actual_lines = {line.strip() for line in f if line.strip()}

    missing = expected_lines - actual_lines
    extra = actual_lines - expected_lines

    assert not missing, f"Missing expected lines in project_log.txt: {missing}"
    assert not extra, f"Unexpected extra lines in project_log.txt: {extra}"

def test_staging_directory_empty():
    staging_dir = "/home/user/staging"
    if os.path.isdir(staging_dir):
        files = os.listdir(staging_dir)
        assert len(files) == 0, f"Files were not moved out of staging directory: {files}"

def test_incoming_directory_empty():
    incoming_dir = "/home/user/incoming"
    if os.path.isdir(incoming_dir):
        files = [f for f in os.listdir(incoming_dir) if f.endswith('.bin')]
        assert len(files) == 0, f"Binary files were not deleted from incoming directory after processing: {files}"