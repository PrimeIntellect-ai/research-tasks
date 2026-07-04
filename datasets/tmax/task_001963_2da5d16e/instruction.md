You are a forensics analyst investigating a compromised Linux host. The attacker exploited an open redirect vulnerability in the login flow of a local Python web application to steal credentials and drop a persistence mechanism. 

You need to perform three recovery and remediation tasks:

1. **Payload Decoding**: 
The attacker left a log of encoded open-redirect payloads in `/home/user/forensics/encoded_payloads.log`. Each line contains a base64-encoded URL. 
Write a Python script (or use shell commands) to decode these URLs, extract just the domain names (e.g., `evil.com` from `https://evil.com/steal?token=123`), and save the unique, alphabetically sorted domain names to `/home/user/forensics/domains.txt`, with one domain per line.

2. **SSH Key Management**: 
The attacker added a backdoor SSH key. Examine the `/home/user/.ssh/authorized_keys` file. Remove any key that does NOT have the comment `analyst@soc.local`. Save the cleaned file containing only the valid key to `/home/user/forensics/clean_authorized_keys`. Ensure the file has no trailing empty lines other than the standard newline after the key.

3. **Content Security Policy (CSP) Testing**:
The vulnerable Flask application is located at `/home/user/app/app.py`. The developers claim they have patched the vulnerability by adding a Content Security Policy header. 
Write a Python unit test using the `unittest` framework in the file `/home/user/app/test_security.py`. 
Your test must:
- Import the Flask app from `app` (i.e., `from app import app`).
- Use the Flask test client to make a `GET` request to the `/login` endpoint.
- Assert that the response contains the `Content-Security-Policy` header.
- Assert that the value of the `Content-Security-Policy` header is exactly `default-src 'self'; script-src 'self'`.

Complete all three tasks. We will verify by checking `domains.txt`, `clean_authorized_keys`, and by running `python3 -m unittest /home/user/app/test_security.py`.