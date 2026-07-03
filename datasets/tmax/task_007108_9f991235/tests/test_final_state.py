# test_final_state.py
import os
import re
import stat
import pytest

SCRIPT_PATH = "/home/user/analyze_redirects.sh"
OUTPUT_PATH = "/home/user/compromised_sessions.txt"
LOG_PATH = "/home/user/audit_data/access.log"

def test_script_exists_and_executable():
    """Verify that the analysis script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_output_file_exists():
    """Verify that the compromised sessions output file exists."""
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."

def test_output_file_content():
    """Verify that the compromised sessions file contains the correctly extracted and redacted data."""
    assert os.path.isfile(LOG_PATH), f"Source log file {LOG_PATH} is missing."

    # Dynamically compute the expected output from the log file
    expected_lines = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse the log line
            # Format: IP_ADDRESS - - [DATE] "METHOD PATH_WITH_QUERY HTTP_VERSION" STATUS_CODE RESPONSE_SIZE "session_id=TOKEN"
            parts = line.split('"')
            if len(parts) >= 3:
                request_part = parts[1]
                # Extract redirect URL
                redirect_match = re.search(r'redirect=(https?://[^ ]+)', request_part)

                # Extract status code
                post_request_parts = parts[2].strip().split()
                if len(post_request_parts) >= 1:
                    status_code = post_request_parts[0]

                    if redirect_match and status_code == "302":
                        malicious_url = redirect_match.group(1)

                        # Redact IP address
                        ip_match = re.match(r'^(\d+\.\d+\.\d+\.)(\d+)', line)
                        if ip_match:
                            redacted_ip = f"***.***.***.{ip_match.group(2)}"
                            redacted_line = line.replace(ip_match.group(0), redacted_ip, 1)
                        else:
                            redacted_line = line

                        # Redact session_id
                        redacted_line = re.sub(r'session_id=[^"]+', 'session_id=REDACTED', redacted_line)

                        expected_lines.append(f"[{malicious_url}] {redacted_line}")

    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."

    with open(OUTPUT_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output, but found {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"