# test_final_state.py
import os
import glob

def rle_encode(s):
    if not s:
        return ""
    result = []
    count = 1
    prev = s[0]
    for char in s[1:]:
        if char == prev:
            count += 1
        else:
            result.append(f"{count}{prev}")
            prev = char
            count = 1
    result.append(f"{count}{prev}")
    return "".join(result)

def test_chunks_directory_and_files():
    chunks_dir = "/home/user/chunks"
    assert os.path.isdir(chunks_dir), f"Directory {chunks_dir} does not exist."

    chunk_files = sorted(glob.glob(os.path.join(chunks_dir, "x*")))
    assert len(chunk_files) == 4, f"Expected 4 chunk files (e.g., xaa, xab, xac, xad), found {len(chunk_files)}."

    for file_path in chunk_files:
        with open(file_path, "r") as f:
            lines = f.read().splitlines()
        assert len(lines) == 5, f"Chunk file {file_path} should contain exactly 5 lines."
        for i, line in enumerate(lines):
            expected_prefix = f"{i + 1},"
            assert line.startswith(expected_prefix), f"Line {i + 1} in {file_path} does not start with '{expected_prefix}'."

def test_compress_script_executable():
    script_path = "/home/user/compress.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_final_dataset_content():
    raw_path = "/home/user/raw_dataset.txt"
    final_path = "/home/user/final_dataset.rle"

    assert os.path.isfile(raw_path), f"Original dataset {raw_path} is missing."
    assert os.path.isfile(final_path), f"Final dataset {final_path} is missing."

    with open(raw_path, "r") as f:
        raw_lines = f.read().splitlines()

    expected_lines = []
    for i, line in enumerate(raw_lines):
        line_num = (i % 5) + 1
        compressed = rle_encode(line)
        expected_lines.append(f"{line_num},{compressed}")

    with open(final_path, "r") as f:
        final_lines = f.read().splitlines()

    assert len(final_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {final_path}, found {len(final_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, final_lines)):
        assert expected == actual, f"Line {i + 1} in {final_path} is incorrect. Expected '{expected}', got '{actual}'."