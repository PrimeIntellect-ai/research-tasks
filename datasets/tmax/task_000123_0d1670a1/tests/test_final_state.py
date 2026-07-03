# test_final_state.py

import os
import stat
import pytest

def test_cpp_source_exists():
    path = "/home/user/filter_elf.cpp"
    assert os.path.isfile(path), f"C++ source file {path} does not exist."

def test_cpp_binary_exists_and_executable():
    path = "/home/user/filter_elf"
    assert os.path.isfile(path), f"Compiled binary {path} does not exist."
    assert os.stat(path).st_mode & stat.S_IXUSR, f"Compiled binary {path} is not executable."

def test_curated_list_output():
    path = "/home/user/curated_list.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "backend_api-curated",
        "service_worker-curated"
    ]

    assert lines == expected_lines, (
        f"Contents of {path} do not match the expected output. "
        f"Expected: {expected_lines}, but got: {lines}"
    )

def test_curated_list_is_sorted():
    path = "/home/user/curated_list.txt"
    if not os.path.isfile(path):
        pytest.fail(f"Output file {path} does not exist.")

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == sorted(lines), f"The output file {path} is not sorted alphabetically."