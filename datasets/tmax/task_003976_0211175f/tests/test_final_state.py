# test_final_state.py

import os
import pytest

def test_processed_docs_directory_exists():
    assert os.path.isdir("/home/user/processed_docs"), "The /home/user/processed_docs/ directory does not exist."

def test_module_files_content():
    expected_contents = {
        "module_01.md": "Content of Alpha",
        "module_02.md": "Content of Beta",
        "module_03.md": "Content of Delta",
        "module_04.md": "Content of Gamma"
    }

    for filename, expected_text in expected_contents.items():
        filepath = os.path.join("/home/user/processed_docs", filename)
        assert os.path.isfile(filepath), f"File {filename} is missing in /home/user/processed_docs/."
        with open(filepath, "r") as f:
            content = f.read()
        assert expected_text in content, f"File {filename} does not contain the expected text '{expected_text}'."

def test_symlink_current_module():
    symlink_path = "/home/user/processed_docs/current_module.md"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    target = os.readlink(symlink_path)
    # The target could be absolute or relative, but it should point to module_04.md
    assert target.endswith("module_04.md"), f"Symlink {symlink_path} does not point to module_04.md. It points to {target}."

def test_index_file_content():
    index_path = "/home/user/processed_docs/index.txt"
    assert os.path.isfile(index_path), f"Index file {index_path} does not exist."

    with open(index_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "module_01.md",
        "module_02.md",
        "module_03.md",
        "module_04.md"
    ]

    assert lines == expected_lines, f"Index file content does not match expected sorted filenames. Got {lines}"

def test_cpp_program_exists_and_uses_rename():
    cpp_path = "/home/user/make_index.cpp"
    assert os.path.isfile(cpp_path), f"C++ program {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "rename(" in content, "The C++ program does not appear to use the POSIX 'rename()' function for atomic writes."