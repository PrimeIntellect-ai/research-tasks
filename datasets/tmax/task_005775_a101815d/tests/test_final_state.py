# test_final_state.py

import os
import json
import base64
import urllib.parse
import ast
import pytest

def get_expected_malicious_ips(log_file):
    """
    Derives the expected malicious IPs by applying the task's logic
    to the actual traffic logs file.
    """
    with open(log_file, 'r') as f:
        logs = json.load(f)

    malicious_ips = set()

    for log in logs:
        cookies = log.get("cookies", {})
        if "X-Debug-Session" in cookies:
            encoded_payload = cookies["X-Debug-Session"]
            try:
                # Reverse URL encoding then Base64 encoding
                b64_decoded = urllib.parse.unquote(encoded_payload)
                payload = base64.b64decode(b64_decoded).decode('utf-8')

                # Parse AST
                tree = ast.parse(payload)
                is_malicious = False

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name in ("os", "subprocess"):
                                is_malicious = True
                    elif isinstance(node, ast.ImportFrom):
                        if node.module in ("os", "subprocess"):
                            is_malicious = True
                    elif isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name):
                            if node.func.id in ("eval", "exec"):
                                is_malicious = True

                if is_malicious:
                    malicious_ips.add(log.get("source_ip"))
            except Exception:
                # If decoding or parsing fails, we skip as it might not be a valid payload
                pass

    return sorted(list(malicious_ips))

def test_script_exists():
    """Test that the student created the analysis script."""
    script_file = "/home/user/analyze_logs.py"
    assert os.path.exists(script_file), f"The script file {script_file} was not found."
    assert os.path.isfile(script_file), f"The path {script_file} is not a file."

def test_output_file_exists():
    """Test that the output file was generated."""
    output_file = "/home/user/malicious_ips.txt"
    assert os.path.exists(output_file), f"The output file {output_file} was not found. Did the script run successfully?"
    assert os.path.isfile(output_file), f"The path {output_file} is not a file."

def test_malicious_ips_content():
    """Test that the output file contains exactly the expected malicious IPs in the correct order."""
    log_file = "/home/user/traffic_logs.json"
    output_file = "/home/user/malicious_ips.txt"

    expected_ips = get_expected_malicious_ips(log_file)

    with open(output_file, 'r') as f:
        # Read lines, strip whitespace/newlines, ignore empty lines
        actual_ips = [line.strip() for line in f if line.strip()]

    assert actual_ips == expected_ips, (
        f"The contents of {output_file} do not match the expected IPs.\n"
        f"Expected: {expected_ips}\n"
        f"Found:    {actual_ips}\n"
        "Ensure you are extracting unique IPs, sorting them in ascending string order, "
        "and correctly parsing the AST for os/subprocess imports and eval/exec calls."
    )