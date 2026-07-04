# test_final_state.py

import os
import re
import base64
import pytest

SCRIPT_PATH = "/home/user/build_archive.sh"
ARCHIVE_PATH = "/home/user/master_archive.b64"
RAW_DOCS_DIR = "/home/user/raw_docs"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_contains_required_commands():
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    assert "flock" in content, "Script must use 'flock' for file locking."
    assert "&" in content, "Script must use '&' to run processes in the background."
    assert "wait" in content, "Script must use 'wait' to wait for background jobs."

def test_archive_exists():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive {ARCHIVE_PATH} does not exist."

def test_archive_contents():
    with open(ARCHIVE_PATH, 'r') as f:
        archive_content = f.read()

    txt_files = [f for f in os.listdir(RAW_DOCS_DIR) if f.endswith('.txt')]
    assert len(txt_files) > 0, "No .txt files found in raw_docs."

    for filename in txt_files:
        filepath = os.path.join(RAW_DOCS_DIR, filename)
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Remove empty lines and vowels
        processed_lines = []
        for line in lines:
            line = line.strip('\n')
            if not line:
                continue
            # Remove vowels
            line = re.sub(r'[aeiouAEIOU]', '', line)
            processed_lines.append(line)

        processed_text = '\n'.join(processed_lines) + '\n'
        encoded_bytes = base64.b64encode(processed_text.encode('utf-8'))
        encoded_str = encoded_bytes.decode('utf-8')

        # The base64 command might wrap lines, but for these short strings, it shouldn't matter.
        # However, the student's base64 output might contain newlines.
        # Let's extract the section from the archive.

        pattern = rf"---\[{re.escape(filename)}\]---\n(.*?)\n---\[EOF\]---"
        match = re.search(pattern, archive_content, re.DOTALL)

        assert match is not None, f"Archive is missing the correct format or entry for {filename}."

        actual_b64 = match.group(1).replace('\n', '')
        assert actual_b64 == encoded_str, f"Base64 content for {filename} does not match expected."