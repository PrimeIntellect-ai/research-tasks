# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_build_script_exists_and_executable():
    build_script = "/home/user/project/build.sh"
    assert os.path.isfile(build_script), f"Build script missing at {build_script}"

    # Check if executable
    st = os.stat(build_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"Build script at {build_script} is not executable"

def test_test_script_exists():
    test_script = "/home/user/project/test_sensor.py"
    assert os.path.isfile(test_script), f"Test script missing at {test_script}"

def test_build_and_test_execution():
    build_script = "/home/user/project/build.sh"
    test_script = "/home/user/project/test_sensor.py"

    # Run build.sh
    result_build = subprocess.run([build_script], cwd="/home/user/project", capture_output=True, text=True)
    assert result_build.returncode == 0, f"build.sh failed with output:\n{result_build.stderr}\n{result_build.stdout}"

    # Check generated files
    go_gen_file = "/home/user/project/gen/go/sensor.pb.go"
    py_gen_file = "/home/user/project/gen/python/sensor_pb2.py"

    assert os.path.isfile(go_gen_file), f"Go generated protobuf missing at {go_gen_file}"
    assert os.path.isfile(py_gen_file), f"Python generated protobuf missing at {py_gen_file}"

    # Run test_sensor.py
    result_test = subprocess.run(["python3", test_script], cwd="/home/user/project", capture_output=True, text=True)
    assert result_test.returncode == 0, f"test_sensor.py failed with output:\n{result_test.stderr}\n{result_test.stdout}"

    # Check log file
    log_file = "/home/user/project/build.log"
    assert os.path.isfile(log_file), f"Log file missing at {log_file}"

    with open(log_file, "r") as f:
        log_content = f.read()

    assert "BUILD_AND_TEST_SUCCESS" in log_content, "Log file does not contain the expected success string."