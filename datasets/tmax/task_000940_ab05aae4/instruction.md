You are a security auditor tasked with reviewing and securing a custom authentication service. The service is designed to receive encoded payloads over a network, decode them, authenticate users, and process basic commands in a sandboxed environment.

A previous developer left the source code for this service in a vendored package at `/app/tinyserver-0.1`. During a preliminary port scan and service audit, you discovered that the service crashes when receiving oversized encoded payloads, and bypasses authentication for certain privileged accounts.

Your objective is to:
1. Audit the C source code in `/app/tinyserver-0.1` (specifically looking at payload decoding and authentication flows).
2. Identify the buffer overflow vulnerability in the custom decoding routine and the logic flaw in the authentication mechanism.
3. Patch the vulnerabilities in the C code to ensure robust input validation and secure authentication. The service must not crash on malicious payloads and must correctly reject invalid credentials.
4. Ensure the service still successfully processes valid, properly encoded payloads and drops privileges as intended.
5. Recompile the service using the provided `Makefile`.
6. Copy the final, patched executable to `/home/user/tinyserver_patched`.

To verify your fix, you can run the evaluation script located at `/app/evaluate_server.py /home/user/tinyserver_patched`. This script will launch your patched binary, send a mix of valid and adversarial payloads, and output an accuracy score between 0.0 and 1.0 based on correct behavior (accepting valid users, rejecting invalid ones, and surviving buffer overflow attempts). 

You must achieve an accuracy score of 1.0. Do not modify `/app/evaluate_server.py` or the test payloads.