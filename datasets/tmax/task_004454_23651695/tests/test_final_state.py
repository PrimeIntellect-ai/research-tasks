# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_app_compiled_and_executable():
    app_path = os.path.join(PROJECT_DIR, "app")
    assert os.path.isfile(app_path), f"Executable {app_path} does not exist."
    assert os.access(app_path, os.X_OK), f"File {app_path} is not executable."

def test_app_output():
    app_path = os.path.join(PROJECT_DIR, "app")
    try:
        result = subprocess.run([app_path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running {app_path} failed with return code {e.returncode} and output: {e.output}")

    expected_output = "Secret: 1123\nUtils loaded.\n"
    assert result.stdout == expected_output, f"App output did not match expected.\nExpected:\n{expected_output}\nGot:\n{result.stdout}"

def test_bash_script_exists():
    sh_script = os.path.join(PROJECT_DIR, "serialize_meta.sh")
    assert os.path.isfile(sh_script), f"Bash script {sh_script} does not exist."

def test_metadata_output():
    metadata_path = os.path.join(PROJECT_DIR, "metadata.txt")
    assert os.path.isfile(metadata_path), f"Metadata file {metadata_path} does not exist."

    expected_content = (
        "FILE: main.c\n"
        "TAGS: 2\n"
        "author=alice\n"
        "version=1.2\n"
        "FILE: utils.c\n"
        "TAGS: 2\n"
        "module=utils\n"
        "status=stable\n"
        "FILE: utils.h\n"
        "TAGS: 0\n"
    )

    with open(metadata_path, "r") as f:
        content = f.read()

    assert content == expected_content, f"Content of {metadata_path} did not match expected.\nExpected:\n{expected_content}\nGot:\n{content}"