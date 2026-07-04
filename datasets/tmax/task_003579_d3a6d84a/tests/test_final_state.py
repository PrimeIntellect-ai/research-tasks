# test_final_state.py

import os
import stat
import pytest

SCRIPT_PATH = "/home/user/compile_docs.py"
OUTPUT_PATH = "/home/user/compiled_docs.md"

EXPECTED_MARKDOWN = """## Initial Setup
*2023-10-01*

Set up the core repository.
Added initial README.

## API v2 Deployment
*2023-10-04*

Deployed the new v2 endpoints to production.
No downtime observed.

## Database Migration
*2023-10-05*

Migrated the users table to PostgreSQL.
Updated the connection strings."""

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_contains_required_functions():
    with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "fcntl.flock" in content, "Script does not use fcntl.flock as required."
    assert "os.replace" in content or "shutil.move" in content, "Script does not use os.replace or shutil.move for atomic updates."

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Compiled documentation {OUTPUT_PATH} does not exist. Did you run the script?"

def test_output_file_content():
    with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # Normalize line endings to avoid issues with \r\n vs \n
    content_normalized = "\n".join(line.rstrip() for line in content.splitlines())
    expected_normalized = "\n".join(line.rstrip() for line in EXPECTED_MARKDOWN.splitlines())

    assert content_normalized == expected_normalized, f"Contents of {OUTPUT_PATH} do not match the expected format and sorting."