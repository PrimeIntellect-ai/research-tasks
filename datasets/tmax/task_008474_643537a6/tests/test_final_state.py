# test_final_state.py

import os
import struct

WORKSPACE_DIR = "/home/user/workspace"
INCLUDE_DIR = os.path.join(WORKSPACE_DIR, "include")
FINAL_BIN = "/home/user/final.bin"

EXPECTED_FILES = ["main.cpp", "utils.cpp", "utils.h"]

def test_workspace_and_files():
    assert os.path.isdir(WORKSPACE_DIR), f"Directory {WORKSPACE_DIR} does not exist."
    for f in EXPECTED_FILES:
        file_path = os.path.join(WORKSPACE_DIR, f)
        assert os.path.isfile(file_path), f"File {file_path} is missing."

def test_file_encoding_and_macros():
    # Check main.cpp
    main_cpp_path = os.path.join(WORKSPACE_DIR, "main.cpp")
    with open(main_cpp_path, "rb") as f:
        content = f.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise AssertionError("main.cpp is not valid UTF-8.")
    assert "NEW_MACRO_ABC" in text, "NEW_MACRO_ABC not found in main.cpp."
    assert "OLD_MACRO_XYZ" not in text, "OLD_MACRO_XYZ still present in main.cpp."
    assert "©" in text, "Copyright symbol not properly decoded as UTF-8 in main.cpp."

    # Check utils.h
    utils_h_path = os.path.join(WORKSPACE_DIR, "utils.h")
    with open(utils_h_path, "rb") as f:
        content = f.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise AssertionError("utils.h is not valid UTF-8.")
    assert "NEW_MACRO_ABC" in text, "NEW_MACRO_ABC not found in utils.h."
    assert "OLD_MACRO_XYZ" not in text, "OLD_MACRO_XYZ still present in utils.h."
    assert "Función" in text, "Special character not properly decoded as UTF-8 in utils.h."

    # Check utils.cpp
    utils_cpp_path = os.path.join(WORKSPACE_DIR, "utils.cpp")
    with open(utils_cpp_path, "rb") as f:
        content = f.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise AssertionError("utils.cpp is not valid UTF-8.")
    assert "Más" in text, "Special character not properly decoded as UTF-8 in utils.cpp."

def test_symlinks():
    assert os.path.isdir(INCLUDE_DIR), f"Directory {INCLUDE_DIR} does not exist."
    symlink_path = os.path.join(INCLUDE_DIR, "utils.h")
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    target = os.readlink(symlink_path)
    # The target can be relative or absolute, but it must resolve to the correct file
    abs_target = os.path.abspath(os.path.join(INCLUDE_DIR, target))
    expected_target = os.path.join(WORKSPACE_DIR, "utils.h")
    assert abs_target == expected_target, f"Symlink {symlink_path} points to {abs_target}, expected {expected_target}."

def test_final_bin_format():
    assert os.path.isfile(FINAL_BIN), f"{FINAL_BIN} is missing."

    with open(FINAL_BIN, "rb") as f:
        data = f.read()

    offset = 0
    parsed_files = []

    while offset < len(data):
        if offset + 1 > len(data):
            raise AssertionError("Unexpected end of file while reading filename length.")

        name_len = data[offset]
        offset += 1

        if offset + name_len > len(data):
            raise AssertionError("Unexpected end of file while reading filename.")

        filename = data[offset:offset+name_len].decode("ascii")
        offset += name_len

        if offset + 4 > len(data):
            raise AssertionError("Unexpected end of file while reading file size.")

        file_size = struct.unpack("<I", data[offset:offset+4])[0]
        offset += 4

        if offset + file_size > len(data):
            raise AssertionError("Unexpected end of file while reading file contents.")

        file_content = data[offset:offset+file_size]
        offset += file_size

        parsed_files.append((filename, file_content))

    # Check alphabetical order
    filenames = [f[0] for f in parsed_files]
    assert filenames == sorted(filenames), f"Files in {FINAL_BIN} are not in alphabetical order. Found: {filenames}"

    # Check contents match the workspace files
    expected_filenames = sorted(EXPECTED_FILES)
    assert filenames == expected_filenames, f"Expected files {expected_filenames} in {FINAL_BIN}, but got {filenames}."

    for filename, content in parsed_files:
        workspace_file = os.path.join(WORKSPACE_DIR, filename)
        with open(workspace_file, "rb") as f:
            expected_content = f.read()
        assert content == expected_content, f"Content of {filename} in {FINAL_BIN} does not match the file in workspace."