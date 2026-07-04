# test_final_state.py

import os
import urllib.parse

def test_files_exist_and_permissions():
    c_file = "/home/user/libmath_encode.c"
    so_file = "/home/user/libmath_encode.so"
    script_file = "/home/user/process_request"

    assert os.path.isfile(c_file), f"C source file {c_file} is missing."
    assert os.path.isfile(so_file), f"Shared library {so_file} is missing."
    assert os.path.isfile(script_file), f"Script file {script_file} is missing."
    assert os.access(script_file, os.X_OK), f"Script file {script_file} is not executable."

def test_result_file_content():
    request_file_path = "/home/user/request.txt"
    result_file_path = "/home/user/result.txt"

    assert os.path.isfile(request_file_path), f"File {request_file_path} is missing."
    assert os.path.isfile(result_file_path), f"File {result_file_path} is missing."

    # Read and parse the request URL to dynamically compute the expected output
    with open(request_file_path, "r") as f:
        url = f.read().strip()

    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    assert "data" in query_params, "URL in request.txt is missing the 'data' parameter."
    assert "key" in query_params, "URL in request.txt is missing the 'key' parameter."

    data = query_params["data"][0]
    key = int(query_params["key"][0])

    # Compute the expected hex string
    expected_hex = ""
    for i, char in enumerate(data):
        encoded_byte = (ord(char) * key + i) % 256
        expected_hex += f"{encoded_byte:02x}"

    # Read the actual result
    with open(result_file_path, "r") as f:
        actual_hex = f.read().strip()

    assert actual_hex == expected_hex, (
        f"Content of {result_file_path} is incorrect.\n"
        f"Expected: '{expected_hex}'\n"
        f"Got:      '{actual_hex}'"
    )