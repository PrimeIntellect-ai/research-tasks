# test_final_state.py

import os

def test_compiled_docs_exists():
    """Verify that the compiled documentation file exists."""
    file_path = "/home/user/compiled_docs.md"
    assert os.path.exists(file_path), f"File {file_path} does not exist. Did you create it?"
    assert os.path.isfile(file_path), f"Path {file_path} is not a regular file."

def test_compiled_docs_content():
    """Verify that the compiled documentation file has the correct content."""
    file_path = "/home/user/compiled_docs.md"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    expected_content = (
        "# api.md\n"
        "This is the API documentation.\n"
        "# architecture.md\n"
        "Architecture diagrams and notes.\n"
        "# deployment.md\n"
        "Miscellaneous deployment notes.\n"
        "# setup.md\n"
        "Setup instructions.\n"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        f"Content of {file_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )