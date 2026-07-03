# test_final_state.py

import os
import json
import stat
import pytest

PROJECT_DIR = "/home/user/project"
BIN_DIR = os.path.join(PROJECT_DIR, "bin")

def test_build_script_exists_and_executable():
    build_script = os.path.join(PROJECT_DIR, "build.sh")
    assert os.path.isfile(build_script), f"{build_script} does not exist."
    st = os.stat(build_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"{build_script} is not executable."

@pytest.mark.parametrize("lib_name", [
    "libC.so",
    "libB.so",
    "libA.so",
])
def test_shared_libraries_exist(lib_name):
    lib_path = os.path.join(BIN_DIR, lib_name)
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not built or is missing."

def test_mock_config_json():
    config_path = os.path.join(PROJECT_DIR, "mock_config.json")
    assert os.path.isfile(config_path), f"{config_path} does not exist."

    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{config_path} does not contain valid JSON.")

    expected_config = {"environment": "CI", "strict_mode": True}
    assert config == expected_config, f"{config_path} content {config} does not match expected {expected_config}."

def test_test_diff_patch_empty():
    patch_path = os.path.join(PROJECT_DIR, "test_diff.patch")
    assert os.path.isfile(patch_path), f"{patch_path} does not exist."

    file_size = os.path.getsize(patch_path)
    assert file_size == 0, f"{patch_path} is not empty (size is {file_size} bytes). This indicates the diff found differences."