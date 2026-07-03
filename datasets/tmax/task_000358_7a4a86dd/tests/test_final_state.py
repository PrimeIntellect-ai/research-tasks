# test_final_state.py
import os
import subprocess

PROJECT_DIR = "/home/user/project"
SRC_DIR = os.path.join(PROJECT_DIR, "src")
INCLUDE_DIR = os.path.join(PROJECT_DIR, "include")
MAKEFILE = os.path.join(PROJECT_DIR, "Makefile")
BENCHMARK_SH = os.path.join(PROJECT_DIR, "benchmark.sh")
SORTED_OUTPUT = os.path.join(PROJECT_DIR, "sorted_output.txt")
HTTP_PARSER = os.path.join(PROJECT_DIR, "http_parser")

def test_directories_exist():
    assert os.path.isdir(SRC_DIR), f"Directory {SRC_DIR} does not exist."
    assert os.path.isdir(INCLUDE_DIR), f"Directory {INCLUDE_DIR} does not exist."

def test_files_moved():
    assert os.path.isfile(os.path.join(SRC_DIR, "main.c")), "main.c was not moved to src/"
    assert os.path.isfile(os.path.join(SRC_DIR, "parser.c")), "parser.c was not moved to src/"
    assert os.path.isfile(os.path.join(INCLUDE_DIR, "parser.h")), "parser.h was not moved to include/"

    # Ensure they don't exist in the root anymore
    assert not os.path.exists(os.path.join(PROJECT_DIR, "main.c")), "main.c should not be in the project root."
    assert not os.path.exists(os.path.join(PROJECT_DIR, "parser.c")), "parser.c should not be in the project root."
    assert not os.path.exists(os.path.join(PROJECT_DIR, "parser.h")), "parser.h should not be in the project root."

def test_benchmark_script_exists_and_executable():
    assert os.path.isfile(BENCHMARK_SH), f"{BENCHMARK_SH} does not exist."
    assert os.access(BENCHMARK_SH, os.X_OK), f"{BENCHMARK_SH} is not executable."

def test_makefile_compiles():
    # Run make clean
    subprocess.run(["make", "clean"], cwd=PROJECT_DIR, capture_output=True)

    # Run make
    result = subprocess.run(["make"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Makefile failed to compile:\n{result.stderr}"

    assert os.path.isfile(HTTP_PARSER), f"Binary {HTTP_PARSER} was not created by make."

def test_sorted_output_correct():
    expected_output = [
        "Method: DELETE, URI: /api/v1/users/123, Version: HTTP/1.1",
        "Method: GET, URI: /api/v1/users, Version: HTTP/1.1",
        "Method: GET, URI: /health, Version: HTTP/1.1",
        "Method: POST, URI: /api/v1/login, Version: HTTP/1.1",
        "Method: PUT, URI: /api/v1/settings, Version: HTTP/1.0"
    ]

    assert os.path.isfile(SORTED_OUTPUT), f"{SORTED_OUTPUT} does not exist. Did you run benchmark.sh?"

    with open(SORTED_OUTPUT, "r") as f:
        actual_output = [line.strip() for line in f if line.strip()]

    assert actual_output == expected_output, f"Sorted output does not match expected output.\nExpected:\n{expected_output}\nActual:\n{actual_output}"

def test_memory_management_fixed():
    parser_c_path = os.path.join(SRC_DIR, "parser.c")
    with open(parser_c_path, "r") as f:
        content = f.read()

    # Check if strdup or malloc is used for string duplication
    has_allocation = "strdup" in content or "malloc" in content
    assert has_allocation, "parser.c does not seem to allocate memory for the parsed strings (e.g., using strdup)."

    # Check if free is called for the strings in free_requests
    # We expect at least multiple frees in the file, specifically inside a loop in free_requests
    assert content.count("free(") >= 3, "parser.c does not seem to free the allocated strings in free_requests."