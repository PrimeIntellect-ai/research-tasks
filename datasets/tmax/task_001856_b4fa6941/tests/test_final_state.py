# test_final_state.py
import os
import hashlib

def test_processed_dir_exists():
    assert os.path.isdir("/home/user/processed_backups"), "Directory /home/user/processed_backups/ was not created."

def test_manifest_content():
    manifest_path = "/home/user/processed_backups/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    raw_dir = "/home/user/raw_backups"
    assert os.path.isdir(raw_dir), "Original raw_backups directory is missing."

    expected_lines = []
    files = sorted([f for f in os.listdir(raw_dir) if f.endswith('.dat')])

    for filename in files:
        filepath = os.path.join(raw_dir, filename)
        with open(filepath, "rb") as f:
            header = f.read(16)
            sha256_hex = hashlib.sha256(header).hexdigest()
            expected_lines.append(f"{filename} {sha256_hex}")

    expected_manifest = "\n".join(expected_lines) + "\n"

    with open(manifest_path, "r") as f:
        actual_manifest = f.read()

    assert actual_manifest.strip() == expected_manifest.strip(), "The contents of manifest.txt do not match the expected output."

def test_hard_links_and_inodes():
    processed_dir = "/home/user/processed_backups"

    file_a = os.path.join(processed_dir, "file_A.dat")
    file_b = os.path.join(processed_dir, "file_B.dat")
    file_c = os.path.join(processed_dir, "file_C.dat")
    file_d = os.path.join(processed_dir, "file_D.dat")

    for f in [file_a, file_b, file_c, file_d]:
        assert os.path.isfile(f), f"File {f} is missing from processed_backups."

    inode_a = os.stat(file_a).st_ino
    inode_b = os.stat(file_b).st_ino
    inode_c = os.stat(file_c).st_ino
    inode_d = os.stat(file_d).st_ino

    assert inode_a == inode_c, "file_C.dat is not a hard link to file_A.dat (inodes differ)."
    assert inode_a != inode_b, "file_A.dat and file_B.dat should not be hard linked."
    assert inode_a != inode_d, "file_A.dat and file_D.dat should not be hard linked."
    assert inode_b != inode_d, "file_B.dat and file_D.dat should not be hard linked."
    assert inode_b != inode_c, "file_B.dat and file_C.dat should not be hard linked."

def test_file_contents():
    raw_dir = "/home/user/raw_backups"
    processed_dir = "/home/user/processed_backups"

    for filename in ["file_A.dat", "file_B.dat", "file_D.dat"]:
        raw_path = os.path.join(raw_dir, filename)
        proc_path = os.path.join(processed_dir, filename)

        with open(raw_path, "rb") as f:
            raw_content = f.read()
        with open(proc_path, "rb") as f:
            proc_content = f.read()

        assert raw_content == proc_content, f"Content of {filename} in processed_backups does not match original."