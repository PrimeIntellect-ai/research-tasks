# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_json_filter_adversarial_corpus():
    """
    Test the standalone JSON payload filter against the clean and evil corpora.
    Evil corpus files must be rejected (exit code 1).
    Clean corpus files must be accepted (exit code 0).
    """
    filter_path = "/home/user/json_filter"
    assert os.path.isfile(filter_path), f"Executable {filter_path} not found."
    assert os.access(filter_path, os.X_OK), f"{filter_path} is not executable."

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]

    assert evil_files, f"No JSON files found in {evil_dir}"
    assert clean_files, f"No JSON files found in {clean_dir}"

    evil_bypassed = []
    for ef in evil_files:
        res = subprocess.run([filter_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(ef))

    clean_modified = []
    for cf in clean_files:
        res = subprocess.run([filter_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(cf))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_memory_leak_fixed():
    """
    Compile a test harness with the user's modified json11.cpp and run it through Valgrind
    to ensure the memory leak has been fixed when parsing an evil payload.
    """
    cpp_file = "/app/vendor/json11/json11.cpp"
    assert os.path.isfile(cpp_file), f"{cpp_file} is missing."

    evil_dir = "/app/corpora/evil"
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]
    assert evil_files, "No evil corpus files found to test memory leak."

    # Use one of the evil files to test the leak fix
    test_file = evil_files[0]

    harness_code = """
#include "json11.hpp"
#include <fstream>
#include <sstream>
#include <string>

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    std::ifstream t(argv[1]);
    std::stringstream buffer;
    buffer << t.rdbuf();
    std::string err;
    json11::Json::parse(buffer.str(), err);
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        harness_path = os.path.join(tmpdir, "harness.cpp")
        with open(harness_path, "w") as f:
            f.write(harness_code)

        exe_path = os.path.join(tmpdir, "harness")
        compile_cmd = ["g++", "-std=c++11", "-I/app/vendor/json11", cpp_file, harness_path, "-o", exe_path]
        res = subprocess.run(compile_cmd, capture_output=True, text=True)
        assert res.returncode == 0, f"Failed to compile test harness with user's json11.cpp: {res.stderr}"

        valgrind_cmd = [
            "valgrind",
            "--leak-check=full",
            "--errors-for-leak-kinds=definite",
            "--error-exitcode=1",
            exe_path,
            test_file
        ]
        res = subprocess.run(valgrind_cmd, capture_output=True, text=True)
        assert res.returncode == 0, f"Memory leak detected by valgrind on {test_file}:\n{res.stderr}"