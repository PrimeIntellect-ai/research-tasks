# test_final_state.py
import os
import pytest
import filecmp

def test_rust_project_exists():
    assert os.path.isfile('/home/user/curator/Cargo.toml'), "Rust project Cargo.toml is missing in /home/user/curator"

def test_rust_source_code_uses_rename():
    src_dir = '/home/user/curator/src'
    assert os.path.isdir(src_dir), "Rust source directory /home/user/curator/src is missing"

    rename_found = False
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.rs'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'rename' in content:
                        rename_found = True
                        break
        if rename_found:
            break

    assert rename_found, "The Rust source code does not contain a call to 'rename' (atomic write constraint not respected)."

def test_curated_directory_contents():
    curated_dir = '/home/user/curated'
    assert os.path.isdir(curated_dir), "The /home/user/curated directory is missing."

    files_in_curated = set(os.listdir(curated_dir))

    # Check exact files
    expected_files = {'bin1', 'bin2'}

    # Filter out anything that might be a directory just in case, though the spec says exactly two files
    actual_files = {f for f in files_in_curated if os.path.isfile(os.path.join(curated_dir, f))}

    assert actual_files == expected_files, f"Expected exactly {expected_files} in /home/user/curated, but found {actual_files}"

def test_curated_files_match_artifacts():
    # Check bin1
    assert filecmp.cmp('/home/user/artifacts/bin1', '/home/user/curated/bin1', shallow=False), "Contents of bin1 do not match the original."

    # Check bin2
    assert filecmp.cmp('/home/user/artifacts/dir1/dir2/bin2', '/home/user/curated/bin2', shallow=False), "Contents of bin2 do not match the original."

def test_no_tmp_files():
    curated_dir = '/home/user/curated'
    if os.path.isdir(curated_dir):
        files_in_curated = os.listdir(curated_dir)
        tmp_files = [f for f in files_in_curated if f.endswith('.tmp')]
        assert not tmp_files, f"Temporary files found in /home/user/curated: {tmp_files}"

def test_invalid_files_not_copied():
    curated_dir = '/home/user/curated'
    assert not os.path.exists(os.path.join(curated_dir, 'bin_32')), "32-bit ELF was incorrectly copied."
    assert not os.path.exists(os.path.join(curated_dir, 'readme.txt')), "Plain text file was incorrectly copied."
    assert not os.path.exists(os.path.join(curated_dir, 'short')), "Malformed short file was incorrectly copied."