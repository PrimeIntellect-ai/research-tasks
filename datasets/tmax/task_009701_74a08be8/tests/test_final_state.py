# test_final_state.py
import os
import pytest

def test_c_program_exists():
    assert os.path.isfile('/home/user/project/organizer.c'), "The C source code '/home/user/project/organizer.c' does not exist."

def test_compiled_program_exists():
    assert os.path.isfile('/home/user/project/organizer'), "The compiled program '/home/user/project/organizer' does not exist."
    assert os.access('/home/user/project/organizer', os.X_OK), "The compiled program '/home/user/project/organizer' is not executable."

def test_target_directories_exist():
    dirs = [
        '/home/user/project/organized/textures',
        '/home/user/project/organized/objects',
        '/home/user/project/organized/archives'
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Target directory '{d}' does not exist."

def test_files_moved_correctly():
    expected_files = {
        '/home/user/project/organized/textures/file_a.dat': b'\x89\x50\x4e\x47',
        '/home/user/project/organized/objects/file_b.dat': b'\xca\xfe\xba\xbe',
        '/home/user/project/organized/archives/file_c.dat': b'\x50\x4b\x03\x04',
        '/home/user/project/organized/textures/file_d.dat': b'\x89\x50\x4e\x47',
        '/home/user/project/dump/file_unknown.dat': b'\x00\x00\x00\x00'
    }

    for path, magic in expected_files.items():
        assert os.path.isfile(path), f"Expected file '{path}' is missing."
        with open(path, 'rb') as f:
            content = f.read(4)
            assert content.lower() == magic.lower(), f"File '{path}' has incorrect magic bytes."

def test_files_removed_from_dump():
    unexpected_files = [
        '/home/user/project/dump/file_a.dat',
        '/home/user/project/dump/file_b.dat',
        '/home/user/project/dump/file_c.dat',
        '/home/user/project/dump/file_d.dat'
    ]
    for path in unexpected_files:
        assert not os.path.exists(path), f"File '{path}' should have been moved out of the dump directory."