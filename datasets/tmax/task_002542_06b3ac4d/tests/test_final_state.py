# test_final_state.py

import os

def test_report_log_exists_and_content():
    report_path = '/home/user/report.log'
    assert os.path.exists(report_path), f"The file {report_path} does not exist."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

    expected_lines = [
        "[ELF] /home/user/project_root/assets/binary.txt",
        "[PNG] /home/user/project_root/assets/image.dat",
        "[ZIP] /home/user/project_root/docs/archive.bak"
    ]

    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"The contents of {report_path} do not match the expected output. Got: {lines}"

def test_organized_directories_and_files():
    expected_files = {
        '/home/user/organized/png/image.dat': b'\x89PNG',
        '/home/user/organized/elf/binary.txt': b'\x7FELF',
        '/home/user/organized/zip/archive.bak': b'PK\x03\x04'
    }

    for file_path, magic in expected_files.items():
        assert os.path.exists(file_path), f"The file {file_path} does not exist in the organized directory."
        with open(file_path, 'rb') as f:
            content = f.read(4)
            assert content == magic, f"The file {file_path} does not have the correct magic bytes. Expected {magic}, got {content}."

def test_original_files_untouched():
    original_files = [
        '/home/user/project_root/assets/image.dat',
        '/home/user/project_root/assets/binary.txt',
        '/home/user/project_root/docs/archive.bak',
        '/home/user/project_root/docs/readme.md',
        '/home/user/project_root/short.bin'
    ]

    for file_path in original_files:
        assert os.path.exists(file_path), f"The original file {file_path} is missing, it should have been left untouched."

def test_sorter_cpp_and_executable():
    cpp_path = '/home/user/sorter.cpp'
    exe_path = '/home/user/sorter'

    assert os.path.exists(cpp_path), f"The source file {cpp_path} does not exist."
    assert os.path.exists(exe_path), f"The executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."