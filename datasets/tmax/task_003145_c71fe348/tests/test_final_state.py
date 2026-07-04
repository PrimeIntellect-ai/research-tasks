# test_final_state.py
import os

def test_files_extracted_safely():
    """Test that files are extracted to the correct safe paths, neutralizing directory traversal."""
    expected_files = [
        "/home/user/docs_safe/docs/index.txt",
        "/home/user/docs_safe/styles/main.css"
    ]

    for file_path in expected_files:
        assert os.path.exists(file_path), f"Expected file {file_path} is missing. Path traversal may not have been neutralized correctly or extraction failed."
        assert os.path.isfile(file_path), f"Expected {file_path} to be a file."

def test_files_utf8_encoded():
    """Test that extracted files are correctly converted to UTF-8."""
    index_path = "/home/user/docs_safe/docs/index.txt"
    css_path = "/home/user/docs_safe/styles/main.css"

    # Check index.txt
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            index_content = f.read()
    except UnicodeDecodeError:
        assert False, f"{index_path} is not valid UTF-8. Encoding conversion failed."

    assert "Welcome to the documentation." in index_content, f"Content of {index_path} is incorrect."

    # Check main.css
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
    except UnicodeDecodeError:
        assert False, f"{css_path} is not valid UTF-8. Encoding conversion failed."

    assert "body { background: white; }" in css_content, f"Content of {css_path} is incorrect."

def test_warnings_log():
    """Test that the warnings log is correctly parsed and saved in UTF-8."""
    log_path = "/home/user/warnings.log"
    assert os.path.exists(log_path), f"Warnings log {log_path} is missing."

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
    except UnicodeDecodeError:
        assert False, f"{log_path} is not valid UTF-8."

    expected_warnings = (
        "[WARNING] Font missing\n"
        "Falling back to default sans-serif font.\n"
        "Please install the required fonts.\n"
        "[WARNING] Unused stylesheet\n"
        "The main.css file is not linked.\n"
    )

    assert log_content.strip() == expected_warnings.strip(), "The parsed warnings log does not match the expected multi-line warning records."