# test_final_state.py
import os
import subprocess
import time
import pytest

def test_files_exist():
    assert os.path.isfile("/home/user/project/CMakeLists.txt"), "CMakeLists.txt is missing."
    assert os.path.isfile("/home/user/project/run_analysis.py"), "run_analysis.py is missing."

def test_execution_time_and_output():
    script_path = "/home/user/project/run_analysis.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    start = time.time()
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    elapsed_ms = (time.time() - start) * 1000

    assert result.returncode == 0, f"run_analysis.py failed with error:\n{result.stderr}"

    # Check if we got some output
    assert result.stdout.strip(), "run_analysis.py did not produce any output."

    # Assert the metric threshold
    assert elapsed_ms <= 50.0, f"Execution time was {elapsed_ms:.2f} ms, which exceeds the 50.0 ms threshold."

def test_shared_library_exists():
    # The shared library should be compiled somewhere in the project directory
    project_dir = "/home/user/project"
    found_so = False
    for root, dirs, files in os.walk(project_dir):
        if "libaudio_analyzer.so" in files:
            found_so = True
            break

    assert found_so, "libaudio_analyzer.so was not found in /home/user/project or its subdirectories."