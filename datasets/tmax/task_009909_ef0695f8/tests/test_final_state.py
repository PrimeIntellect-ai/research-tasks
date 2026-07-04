# test_final_state.py
import os
import subprocess
import pytest

def test_ci_script_exists_and_executable():
    ci_path = "/home/user/ci.sh"
    assert os.path.exists(ci_path), f"{ci_path} does not exist"
    assert os.access(ci_path, os.X_OK), f"{ci_path} is not executable"

def test_ci_script_execution():
    ci_path = "/home/user/ci.sh"
    # Execute the CI script to generate artifacts
    result = subprocess.run([ci_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"ci.sh failed with return code {result.returncode} and error: {result.stderr}"

def test_artifacts_created():
    assert os.path.exists("/home/user/builder"), "/home/user/builder executable not created"
    assert os.path.exists("/home/user/mem.prof"), "/home/user/mem.prof not created"
    assert os.path.exists("/home/user/build_log.txt"), "/home/user/build_log.txt not created"

def test_build_log_content():
    log_path = "/home/user/build_log.txt"
    assert os.path.exists(log_path), f"{log_path} does not exist"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 8, f"Expected exactly 8 lines in build_log.txt, got {len(lines)}"

    # Check init
    assert lines[0] == "START init 10", f"First line must be 'START init 10', got '{lines[0]}'"
    assert lines[1] == "DONE init", f"Second line must be 'DONE init', got '{lines[1]}'"

    # Check presence of intermediate tasks
    assert "START build_db 4" in lines, "Missing 'START build_db 4'"
    assert "DONE build_db" in lines, "Missing 'DONE build_db'"
    assert "START build_web 6" in lines, "Missing 'START build_web 6'"
    assert "DONE build_web" in lines, "Missing 'DONE build_web'"

    # Check intermediate tasks ordering
    assert lines.index("DONE build_db") > lines.index("START build_db 4"), "DONE build_db must appear after START build_db 4"
    assert lines.index("DONE build_web") > lines.index("START build_web 6"), "DONE build_web must appear after START build_web 6"
    assert lines.index("START build_db 4") > lines.index("DONE init"), "START build_db 4 must appear after DONE init"
    assert lines.index("START build_web 6") > lines.index("DONE init"), "START build_web 6 must appear after DONE init"

    # Check link_all
    assert lines[-2] == "START link_all 12", f"Second to last line must be 'START link_all 12', got '{lines[-2]}'"
    assert lines[-1] == "DONE link_all", f"Last line must be 'DONE link_all', got '{lines[-1]}'"

    # Check that link_all starts after dependencies are done
    assert lines.index("START link_all 12") > lines.index("DONE build_db"), "START link_all 12 must appear after DONE build_db"
    assert lines.index("START link_all 12") > lines.index("DONE build_web"), "START link_all 12 must appear after DONE build_web"