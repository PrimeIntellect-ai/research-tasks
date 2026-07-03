# test_final_state.py
import os

def test_symlink_created():
    symlink_path = "/home/user/latest_dataset"
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."

    target = os.readlink(symlink_path)
    # The target can be absolute or relative, but it must resolve to /home/user/dataset.tar
    assert os.path.abspath(os.path.join("/home/user", target)) == "/home/user/dataset.tar", \
        f"Symlink points to {target}, expected it to point to /home/user/dataset.tar."

def test_safe_files_extracted():
    extract_dir = "/home/user/extracted_safe"
    assert os.path.isdir(extract_dir), f"Directory {extract_dir} does not exist."

    extracted_files = set(os.listdir(extract_dir))
    expected_files = {"safe1.bin", "safe2.dat", "safe_alpha.bin"}

    assert extracted_files == expected_files, \
        f"Expected exactly {expected_files} in {extract_dir}, but found {extracted_files}."

def test_unsafe_files_not_extracted():
    unsafe_paths = [
        "/home/user/evil.txt",
        "/root.bin",
        "/home/evil.txt",
        "/evil.txt"
    ]
    for path in unsafe_paths:
        assert not os.path.exists(path), f"Unsafe file was extracted to {path}!"

def test_headers_txt_content():
    headers_path = "/home/user/headers.txt"
    assert os.path.isfile(headers_path), f"File {headers_path} does not exist."

    with open(headers_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "safe1.bin DEADBEEF",
        "safe2.dat CAFEBABE",
        "safe_alpha.bin 12345678"
    ]

    assert lines == expected_lines, \
        f"Contents of {headers_path} do not match expected output. Got: {lines}"