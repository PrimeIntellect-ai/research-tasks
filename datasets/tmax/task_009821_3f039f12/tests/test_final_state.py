# test_final_state.py

import os
import re
import subprocess
import pytest

def test_build_new_exists_and_format():
    build_new_path = "/home/user/project/build.new"
    assert os.path.isfile(build_new_path), f"File {build_new_path} does not exist."

    with open(build_new_path, "r") as f:
        content = f.read()

    # Check that there are no commas in DEPS lines
    for line in content.splitlines():
        if line.startswith("DEPS"):
            assert "," not in line, f"Found comma in DEPS line: {line}"

    # Check that expected targets are present
    assert "TARGET all" in content, "Missing 'TARGET all' in build.new"
    assert "TARGET frontend" in content, "Missing 'TARGET frontend' in build.new"
    assert "TARGET backend" in content, "Missing 'TARGET backend' in build.new"

    # Check that DEPS are space separated
    assert re.search(r"DEPS\s+frontend\s+backend", content) or re.search(r"DEPS\s+backend\s+frontend", content), "Missing 'DEPS frontend backend' in build.new"

def test_benchmark_log_exists():
    log_path = "/home/user/project/benchmark.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    # Check that all targets were built and logged
    for target in ["all", "frontend", "backend", "ui_components", "database"]:
        assert re.search(rf"^{target}\s+\d+ms", content, re.MULTILINE), f"Target {target} not found in benchmark.log"

def test_minibuild_memory_safety():
    cpp_path = "/home/user/project/minibuild.cpp"
    exe_path = "/home/user/project/minibuild"
    build_new_path = "/home/user/project/build.new"

    assert os.path.isfile(cpp_path), f"File {cpp_path} does not exist."

    # Compile the cpp file
    compile_cmd = ["g++", "-std=c++17", "-O2", cpp_path, "-o", exe_path]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Compilation failed:\n{result.stderr}"

    # Run valgrind
    valgrind_cmd = [
        "valgrind", 
        "--leak-check=full", 
        "--error-exitcode=1", 
        exe_path, 
        build_new_path
    ]
    result = subprocess.run(valgrind_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Valgrind found memory errors or leaks:\n{result.stderr}"