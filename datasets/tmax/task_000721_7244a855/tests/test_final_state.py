# test_final_state.py
import os
import urllib.request
import urllib.error

def test_admin_flag_retrieved():
    """
    Validates Phase 1: The student must have successfully forged the token, 
    accessed the admin dashboard, and saved the flag to the specified file.
    """
    flag_path = '/home/user/admin_flag.txt'

    # Check if the file was created
    assert os.path.isfile(flag_path), f"The file {flag_path} does not exist. Phase 1 is incomplete."

    # Read the contents and verify the flag
    with open(flag_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected_flag = "FLAG{h4ck3d_th3_cbC_m0d3}"
    assert expected_flag in content, (
        f"The file {flag_path} does not contain the correct admin flag. "
        f"Expected to find '{expected_flag}', but found: '{content}'"
    )

def test_csp_header_enforced():
    """
    Validates Phase 2: The student must have modified the Flask app to 
    include the specific Content-Security-Policy header and restarted it.
    """
    url = 'http://127.0.0.1:8080/'

    try:
        # Make a request to the local application
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            headers = response.headers
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to the Flask app at {url}. Did you restart it successfully? Error: {e}"

    # urllib headers.get is case-insensitive for header names
    csp_value = headers.get('Content-Security-Policy')

    assert csp_value is not None, (
        "The 'Content-Security-Policy' header is missing from the HTTP response. "
        "Phase 2 is incomplete."
    )

    expected_csp = "default-src 'self'; script-src 'self'"
    assert csp_value == expected_csp, (
        f"The 'Content-Security-Policy' header value is incorrect.\n"
        f"Expected: {expected_csp}\n"
        f"Actual:   {csp_value}"
    )