# test_final_state.py

import os
import subprocess
import hashlib
import gzip
import stat

def test_c_program_exists():
    assert os.path.isfile('/home/user/zsha256.c'), "C source code /home/user/zsha256.c is missing."

def test_executable_exists():
    executable = '/home/user/zsha256'
    assert os.path.isfile(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_executable_behavior():
    executable = '/home/user/zsha256'
    test_file = '/home/user/repo/art1.gz'

    if not os.path.isfile(executable) or not os.path.isfile(test_file):
        return # Handled by other tests

    result = subprocess.run([executable, test_file], capture_output=True, text=True)
    assert result.returncode == 0, "Executable failed to run on a valid .gz file."

    expected_hash = "72a2e412ddc2941198edcc549ed0f9ca22dd5c192d27464ce7ec017e4bb07c13"
    output = result.stdout.strip()
    assert output == expected_hash, f"Executable output '{output}' did not match expected hash '{expected_hash}'."

def test_curated_directory_exists():
    assert os.path.isdir('/home/user/curated'), "Directory /home/user/curated is missing."

def test_curated_files_exist():
    expected_files = [
        "72a2e412ddc2941198edcc549ed0f9ca22dd5c192d27464ce7ec017e4bb07c13.gz",
        "c864a6eeb1821034bcff24976c66cf10cf54cd7da9c1851e2bc68b8a0dfbcda6.gz",
        "92520330ce9c2e0b503028fb4abef52bf482ab87019310d65ffc4fbcbb0b6c6b.gz",
        "manifest.txt"
    ]

    for f in expected_files:
        path = os.path.join('/home/user/curated', f)
        assert os.path.isfile(path), f"Expected file {path} is missing."

def test_manifest_content():
    manifest_path = '/home/user/curated/manifest.txt'
    assert os.path.isfile(manifest_path), "Manifest file is missing."

    expected_content = (
        "72a2e412ddc2941198edcc549ed0f9ca22dd5c192d27464ce7ec017e4bb07c13 art1.gz\n"
        "92520330ce9c2e0b503028fb4abef52bf482ab87019310d65ffc4fbcbb0b6c6b subdir/art3.gz\n"
        "c864a6eeb1821034bcff24976c66cf10cf54cd7da9c1851e2bc68b8a0dfbcda6 subdir/art2.gz\n"
    )

    with open(manifest_path, 'r') as f:
        content = f.read()

    assert content == expected_content, "Manifest file content does not match the expected sorted output."

def test_curated_gz_files_validity():
    # Ensure the copied files are still valid gzip files and their uncompressed contents match
    expected_data = {
        "72a2e412ddc2941198edcc549ed0f9ca22dd5c192d27464ce7ec017e4bb07c13": b"artifact_one_data",
        "c864a6eeb1821034bcff24976c66cf10cf54cd7da9c1851e2bc68b8a0dfbcda6": b"artifact_two_data_v2",
        "92520330ce9c2e0b503028fb4abef52bf482ab87019310d65ffc4fbcbb0b6c6b": b"artifact_three_data_final"
    }

    for h, data in expected_data.items():
        path = f"/home/user/curated/{h}.gz"
        if os.path.isfile(path):
            with gzip.open(path, 'rb') as f:
                content = f.read()
            assert content == data, f"Uncompressed content of {path} does not match expected data."