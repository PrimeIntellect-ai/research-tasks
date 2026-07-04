# test_final_state.py
import os

def test_c_source_exists():
    c_file = "/home/user/generate_manifest.c"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."

def test_manifest_exists_and_content():
    manifest_file = "/home/user/pending_backups.txt"
    assert os.path.isfile(manifest_file), f"Manifest file {manifest_file} is missing."

    with open(manifest_file, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "audit_logs",
        "order_items",
        "orders"
    ]
    expected_content = "\n".join(expected_lines)

    assert content == expected_content, (
        f"Manifest content does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Got:\n{content}"
    )