# test_final_state.py

import os
import re
import pytest

def test_final_output_log():
    log_path = "/home/user/final_output.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "default: -1\nandroid: 15\nios: 22"
    assert content == expected_content, f"Content of {log_path} does not match expected output.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_mobile_sensor_directory():
    dir_path = "/home/user/mobile_sensor"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

def test_cargo_toml_configuration():
    cargo_path = "/home/user/mobile_sensor/Cargo.toml"
    assert os.path.exists(cargo_path), f"File {cargo_path} does not exist."

    with open(cargo_path, "r") as f:
        content = f.read()

    # Check crate-type
    assert re.search(r'crate-type\s*=\s*\[\s*"cdylib"\s*\]', content), "Cargo.toml does not contain crate-type = [\"cdylib\"]."

    # Check libc dependency
    assert re.search(r'libc\s*=', content) or "[dependencies.libc]" in content or "libc" in content, "Cargo.toml does not contain libc as a dependency."

    # Check features
    assert re.search(r'android\s*=', content) or "[features]" in content and "android" in content, "Cargo.toml does not define the 'android' feature."
    assert re.search(r'ios\s*=', content) or "[features]" in content and "ios" in content, "Cargo.toml does not define the 'ios' feature."

def test_run_all_tests_script():
    script_path = "/home/user/run_all_tests.sh"
    assert os.path.exists(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_verify_py_script():
    script_path = "/home/user/verify.py"
    assert os.path.exists(script_path), f"File {script_path} does not exist."

def test_libs_directory_and_files():
    libs_dir = "/home/user/libs"
    assert os.path.isdir(libs_dir), f"Directory {libs_dir} does not exist."

    expected_files = [
        "libmobile_sensor_default.so",
        "libmobile_sensor_android.so",
        "libmobile_sensor_ios.so"
    ]

    for f in expected_files:
        file_path = os.path.join(libs_dir, f)
        assert os.path.exists(file_path), f"Shared library {file_path} does not exist."