# test_final_state.py
import os
import re
import ast

def get_expected_size(base_dir):
    total_size = 0

    for root, _, files in os.walk(base_dir):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith(".log"):
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                # Check for [CRITICAL] on one line and [END CRITICAL] on a subsequent line
                if re.search(r"\[CRITICAL\].*?\[END CRITICAL\]", content, re.DOTALL):
                    total_size += os.path.getsize(filepath)
            elif file.endswith(".dat"):
                size = os.path.getsize(filepath)
                if size >= 1028:
                    with open(filepath, "rb") as f:
                        f.seek(1024)
                        signature = f.read(4)
                        if signature == b'\xde\xad\xbe\xef':
                            total_size += size
    return total_size

def test_script_exists_and_uses_required_modules():
    script_path = "/home/user/find_waste.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "mmap" in content, "The script does not seem to use 'mmap' as required."

    # Check for atomic rename (os.rename, os.replace, shutil.move, Path.rename)
    atomic_keywords = ["rename", "replace", "move"]
    has_atomic = any(kw in content for kw in atomic_keywords)
    assert has_atomic, "The script does not seem to perform an atomic write operation (e.g., using os.rename)."

def test_output_file_content():
    output_path = "/home/user/reclaimable_space.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    base_dir = "/home/user/storage_dumps"
    expected_size = get_expected_size(base_dir)
    expected_content = f"Total bytes: {expected_size}"

    with open(output_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {output_path} is incorrect. "
        f"Expected '{expected_content}', but got '{actual_content}'."
    )