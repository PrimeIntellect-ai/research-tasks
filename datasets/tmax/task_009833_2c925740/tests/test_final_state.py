# test_final_state.py

import os
import hashlib
import stat

def test_c_program_exists():
    c_file = "/home/user/filter_dataset.c"
    assert os.path.isfile(c_file), f"C source file {c_file} does not exist."

def test_executable_exists_and_is_executable():
    exe_file = "/home/user/filter_dataset"
    assert os.path.isfile(exe_file), f"Executable {exe_file} does not exist."
    st = os.stat(exe_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {exe_file} is not executable."

def test_filtered_files_contents():
    expected_contents = {
        "sensor1.txt": "60\n80\n",
        "sensor2.txt": "51\n100\n",
        "sensor3.txt": "200\n"
    }

    for filename, expected_text in expected_contents.items():
        filepath = os.path.join("/home/user/filtered", filename)
        assert os.path.isfile(filepath), f"Filtered file {filepath} does not exist."

        with open(filepath, "r") as f:
            content = f.read()

        # Normalize newlines for robust comparison
        content_lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
        expected_lines = [line.strip() for line in expected_text.strip().split('\n') if line.strip()]

        assert content_lines == expected_lines, f"Content of {filepath} is incorrect. Expected {expected_lines}, got {content_lines}."

def test_manifest_file():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    expected_contents = {
        "sensor1.txt": "60\n80\n",
        "sensor2.txt": "51\n100\n",
        "sensor3.txt": "200\n"
    }

    # Calculate expected hashes based on actual file contents on disk to be robust against newline variations
    expected_manifest_lines = []
    for filename in sorted(expected_contents.keys()):
        filepath = os.path.join("/home/user/filtered", filename)
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                file_bytes = f.read()
            file_hash = hashlib.sha256(file_bytes).hexdigest()
            expected_manifest_lines.append(f"{file_hash}  {filename}")

    with open(manifest_path, "r") as f:
        manifest_content = f.read().strip()

    manifest_lines = [line.strip() for line in manifest_content.split('\n') if line.strip()]

    assert len(manifest_lines) == len(expected_manifest_lines), "Manifest does not contain the correct number of entries."

    for expected_line, actual_line in zip(expected_manifest_lines, manifest_lines):
        assert actual_line == expected_line, f"Manifest line mismatch. Expected '{expected_line}', got '{actual_line}'."