# test_final_state.py
import os

def test_restored_docs_content():
    output_path = "/home/user/restored_docs.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. The script must create this file."

    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_content = "System Architecture Overview\nAPI Integration Guidelines"

    # We strip trailing newlines to be robust against whether the student added a final newline or not,
    # but the separator between the two lines must be exactly one newline.
    assert content.strip() == expected_content, (
        f"The content of {output_path} does not match the expected decompressed text.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )

def test_go_script_exists():
    script_path = "/home/user/restore.go"
    assert os.path.isfile(script_path), f"The Go script at {script_path} is missing."