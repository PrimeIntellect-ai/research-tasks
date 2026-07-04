# test_final_state.py

import os
import stat
import re

SCRIPT_PATH = "/home/user/process_logs.sh"
REPORT_PATH = "/home/user/final_report.csv"

EXPECTED_CSV = """Timestamp,IP,Path,Count
2023-11-15T08:30:00Z,192.168.12.000,/api/v1/users,5
2023-11-15T08:40:00Z,10.0.0.000,/login,2
2023-11-15T08:40:00Z,172.16.5.000,/healthcheck,1
"""

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"Script {SCRIPT_PATH} is not executable."

def test_script_uses_parallel_processing():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    # Look for standard parallel execution constructs
    has_ampersand = re.search(r'&\s*$', content, re.MULTILINE) is not None
    has_ampersand_inline = re.search(r'&\s+', content) is not None
    has_xargs_p = re.search(r'xargs\s+.*?-[P|p]', content) is not None
    has_parallel = re.search(r'\bparallel\b', content) is not None
    has_wait = re.search(r'\bwait\b', content) is not None

    uses_parallel = (has_ampersand and has_wait) or (has_ampersand_inline and has_wait) or has_xargs_p or has_parallel
    assert uses_parallel, "Script does not appear to use parallel processing (e.g., '&' with 'wait', 'xargs -P', or 'parallel')."

def test_final_report_exists_and_matches():
    assert os.path.isfile(REPORT_PATH), f"Final report {REPORT_PATH} does not exist."

    with open(REPORT_PATH, 'r') as f:
        content = f.read()

    assert content.strip() == EXPECTED_CSV.strip(), f"Content of {REPORT_PATH} does not match expected output.\nExpected:\n{EXPECTED_CSV}\nActual:\n{content}"