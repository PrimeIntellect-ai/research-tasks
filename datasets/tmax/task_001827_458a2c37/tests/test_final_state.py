# test_final_state.py

import os
import subprocess
import tempfile

def test_recovered_token():
    token_path = "/home/user/recovered_token.txt"
    assert os.path.exists(token_path), f"{token_path} does not exist."
    with open(token_path, "r") as f:
        content = f.read().strip()
    assert content == "CRASH_TK_99", f"Expected 'CRASH_TK_99' in {token_path}, but got '{content}'."

def test_fuzz_target_exists_and_contains_entrypoint():
    fuzz_target_path = "/home/user/parser_repo/fuzz_target.cc"
    assert os.path.exists(fuzz_target_path), f"{fuzz_target_path} does not exist."
    with open(fuzz_target_path, "r") as f:
        content = f.read()
    assert "LLVMFuzzerTestOneInput" in content, f"{fuzz_target_path} must contain LLVMFuzzerTestOneInput."

def test_parser_cpp_fixed_asan():
    parser_cpp_path = "/home/user/parser_repo/parser.cpp"
    assert os.path.exists(parser_cpp_path), f"{parser_cpp_path} does not exist."

    # Create a test script that feeds a 12-byte payload starting with CRASH_TK_99
    test_cpp = """
#include "parser.h"
#include <cstdint>
#include <vector>

int main() {
    std::vector<uint8_t> payload = {'C','R','A','S','H','_','T','K','_','9','9','X'};
    parse_data(payload.data(), payload.size());
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.cpp")
        with open(test_file, "w") as f:
            f.write(test_cpp)

        executable = os.path.join(tmpdir, "test_bin")

        # Compile with ASAN
        compile_cmd = [
            "clang++", "-g", "-O1", "-fsanitize=address",
            test_file, parser_cpp_path, "-I/home/user/parser_repo", "-o", executable
        ]

        comp = subprocess.run(compile_cmd, capture_output=True, text=True)
        assert comp.returncode == 0, f"Compilation with ASAN failed:\n{comp.stderr}"

        # Run the compiled binary
        run_res = subprocess.run([executable], capture_output=True, text=True)
        assert run_res.returncode == 0, f"Execution failed (likely an ASAN memory error):\n{run_res.stderr}"