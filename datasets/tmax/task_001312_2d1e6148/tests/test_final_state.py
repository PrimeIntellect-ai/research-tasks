# test_final_state.py

import os
import re

def test_root_cause_identified():
    path = "/home/user/root_cause.txt"
    assert os.path.isfile(path), f"Verification failed: {path} not found."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "*", f"Verification failed: root_cause.txt does not correctly identify '*'. Found: {content}"

def test_mre_script_exists():
    path = "/home/user/mre.sh"
    assert os.path.isfile(path), "Verification failed: mre.sh not found."

def test_archiver_fix_no_cat_loop():
    path = "/home/user/archiver.sh"
    assert os.path.isfile(path), f"Verification failed: {path} not found."

    with open(path, "r") as f:
        content = f.read()

    # Check that it no longer uses the vulnerable for-loop construct
    assert not re.search(r"for\s+\w+\s+in\s+\$\(\s*cat", content), \
        "Verification failed: archiver.sh still uses the vulnerable for-loop construct."

def test_archiver_fix_quoted_rm():
    path = "/home/user/archiver.sh"
    assert os.path.isfile(path), f"Verification failed: {path} not found."

    with open(path, "r") as f:
        lines = f.readlines()

    for line in lines:
        # Check if line contains rm and an unquoted $file
        # This regex looks for `rm ` followed by anything that isn't a quote, then `$file`
        if re.search(r'rm\s+[^"]*\$file', line) or re.search(r"rm\s+[^']*\$file", line):
            # To be more precise, if it's unquoted, it won't have quotes around the variable
            # Let's just use the bash validation logic equivalent:
            pass

    with open(path, "r") as f:
        content = f.read()

    # Check archiver fix - should have proper quoting around rm
    # Equivalent to grep -Eq 'rm[[:space:]]+[^"]*\$file'
    assert not re.search(r'rm\s+[^"]*\$file', content), \
        "Verification failed: archiver.sh still contains unquoted rm arguments."