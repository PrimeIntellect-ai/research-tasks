# test_final_state.py

import os
import stat
import subprocess
import pytest

PROJECT_DIR = "/home/user/legacy_project"

def test_output_txt_content():
    output_file = os.path.join(PROJECT_DIR, "output.txt")
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == "2122", f"Expected output.txt to contain '2122', but found '{content}'."

def test_ci_test_sh_exists_and_executable():
    ci_script = os.path.join(PROJECT_DIR, "ci_test.sh")
    assert os.path.isfile(ci_script), f"CI script {ci_script} does not exist."

    st = os.stat(ci_script)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, f"CI script {ci_script} is not executable."

def test_ci_test_sh_execution():
    ci_script = os.path.join(PROJECT_DIR, "ci_test.sh")
    assert os.path.isfile(ci_script), f"CI script {ci_script} does not exist."

    # Remove output.txt to ensure the script regenerates it
    output_file = os.path.join(PROJECT_DIR, "output.txt")
    if os.path.exists(output_file):
        os.remove(output_file)

    result = subprocess.run(["/bin/bash", ci_script], cwd=PROJECT_DIR, capture_output=True)
    assert result.returncode == 0, f"ci_test.sh failed with return code {result.returncode}. Stderr: {result.stderr.decode()}"

    # Verify it recreated output.txt correctly
    assert os.path.isfile(output_file), "ci_test.sh did not generate output.txt."
    with open(output_file, "r") as f:
        content = f.read().strip()
    assert content == "2122", f"After running ci_test.sh, output.txt contains '{content}' instead of '2122'."

def test_main_py_execution():
    main_script = os.path.join(PROJECT_DIR, "main.py")

    # Run python3 main.py directly to ensure no ImportError or TypeError occurs
    result = subprocess.run(["python3", main_script], cwd=PROJECT_DIR, capture_output=True)
    assert result.returncode == 0, f"main.py failed to execute. Stderr: {result.stderr.decode()}"