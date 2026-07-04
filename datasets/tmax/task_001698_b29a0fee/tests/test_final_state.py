# test_final_state.py

import os
import sys
import importlib.util
import base64

def test_flag_file_exists_and_correct():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"Expected flag file {flag_path} does not exist."

    with open(flag_path, "r") as f:
        content = f.read()

    expected_flag = "FLAG{signed_int_fix}"
    assert content == expected_flag, f"Flag file content is incorrect. Expected '{expected_flag}', got '{content}'."

def test_parse_packet_script_fixed():
    script_path = "/home/user/parse_packet.py"
    assert os.path.isfile(script_path), f"Parser script {script_path} is missing."

    # Load the module to test the parse function
    spec = importlib.util.spec_from_file_location("parse_packet", script_path)
    parse_packet = importlib.util.module_from_spec(spec)
    sys.modules["parse_packet"] = parse_packet
    spec.loader.exec_module(parse_packet)

    assert hasattr(parse_packet, "parse"), "parse_packet.py is missing the 'parse' function."

    # The original base64 payload from the log
    b64_payload = "RkxBR3tzaWduZWRfaW50X2ZpeH0A3q2+7+P///8="
    binary_payload = base64.b64decode(b64_payload)

    try:
        result = parse_packet.parse(binary_payload)
    except Exception as e:
        assert False, f"parse_packet.parse() raised an exception: {e}"

    assert result == "FLAG{signed_int_fix}", f"parse_packet.parse() returned incorrect result: {result}. The script might not be correctly handling signed integers."