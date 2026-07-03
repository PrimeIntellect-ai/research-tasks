# test_final_state.py

import os
import re
import subprocess
import pytest

def test_protobuf_file():
    proto_path = "/home/user/aggregator.proto"
    assert os.path.exists(proto_path), f"{proto_path} does not exist."

    with open(proto_path, "r") as f:
        content = f.read()

    # Check syntax and package
    assert re.search(r'syntax\s*=\s*"proto3"\s*;', content), "Missing or incorrect syntax declaration."
    assert re.search(r'package\s+migration\s*;', content), "Missing or incorrect package declaration."

    # Check service
    assert "service Aggregator" in content, "Aggregator service not defined."
    assert re.search(r'rpc\s+Record\s*\(\s*RecordRequest\s*\)\s*returns\s*\(\s*RecordResponse\s*\)', content), "Record RPC not correctly defined."
    assert re.search(r'rpc\s+GetTop\s*\(\s*TopRequest\s*\)\s*returns\s*\(\s*TopResponse\s*\)', content), "GetTop RPC not correctly defined."

    # Check messages
    assert "message RecordRequest" in content, "RecordRequest message not defined."
    assert "message RecordResponse" in content, "RecordResponse message not defined."
    assert "message TopRequest" in content, "TopRequest message not defined."
    assert "message TopResponse" in content, "TopResponse message not defined."

def test_cpp_frequency_store():
    header_path = "/home/user/FrequencyStore.h"
    cpp_path = "/home/user/FrequencyStore.cpp"

    assert os.path.exists(header_path), f"{header_path} does not exist."
    assert os.path.exists(cpp_path), f"{cpp_path} does not exist."

    test_runner_code = """
    #include "/home/user/FrequencyStore.h"
    #include <cassert>
    #include <iostream>

    int main() {
        FrequencyStore store;
        store.record("banana");
        store.record("apple");
        store.record("banana");
        store.record("cherry");
        store.record("apple");
        store.record("apple");

        auto top = store.get_top(2);
        if (top.size() != 2) return 1;
        if (top[0] != "apple") return 2;
        if (top[1] != "banana") return 3;

        // Test tie breaking (lexicographical)
        FrequencyStore store2;
        store2.record("zebra");
        store2.record("alpha");
        auto top2 = store2.get_top(2);
        if (top2.size() != 2) return 4;
        if (top2[0] != "alpha") return 5;
        if (top2[1] != "zebra") return 6;

        return 0;
    }
    """

    runner_path = "/tmp/test_runner.cpp"
    out_binary = "/tmp/test_runner"

    with open(runner_path, "w") as f:
        f.write(test_runner_code)

    compile_res = subprocess.run(
        ["g++", "-std=c++11", runner_path, cpp_path, "-o", out_binary],
        capture_output=True,
        text=True
    )

    assert compile_res.returncode == 0, f"Failed to compile FrequencyStore.cpp:\n{compile_res.stderr}"

    run_res = subprocess.run([out_binary], capture_output=True, text=True)
    assert run_res.returncode == 0, f"C++ logic test failed with return code {run_res.returncode}. Ensure sorting logic is correct."

def test_rust_client_output():
    log_path = "/home/user/rust_output.log"
    assert os.path.exists(log_path), f"{log_path} does not exist. Did you run the Rust client?"

    with open(log_path, "r") as f:
        content = f.read()

    expected_lines = [
        "Recorded: error",
        "Successfully processed log: error",
        "Recorded: warning",
        "Successfully processed log: warning",
        "Recorded: error",
        "Successfully processed log: error",
        "Recorded: info",
        "Successfully processed log: info"
    ]

    for line in expected_lines:
        assert line in content, f"Expected log line '{line}' not found in rust_output.log. Ensure the Rust bug is fixed properly."