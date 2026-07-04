You are a compliance analyst working on generating audit trails and security filters for a legacy authentication microservice. The microservice processes login redirect flows but has been flagged in a recent audit for an Open Redirect vulnerability (CWE-601) and improper payload validation. 

Because we cannot recompile the legacy service, we need to deploy a strict input sanitization/classifier script in front of it.

You have been provided with the legacy service binary at `/app/auth_redirector`. It is a stripped binary that accepts a single base64-encoded payload containing redirect instructions and session tokens. 

Your task is to write a standalone classifier script that evaluates these incoming payloads. 
1. The script must accept exactly one argument: the base64-encoded payload.
2. It must decode and analyze the payload to determine if it is a legitimate internal redirect or a malicious open redirect / payload tampering attempt.
3. If the payload is benign and safe for the legacy binary to process, your script must exit with status code `0`.
4. If the payload is malicious, exploits the open redirect flaw, or contains privilege escalation tokens, your script must exit with status code `1`.

To help you understand what constitutes "safe" versus "malicious" in the context of our legacy system, we have provided two directories containing sample payloads (one base64 string per file):
- `/app/corpora/clean/`: Contains legitimate payloads that must be accepted.
- `/app/corpora/evil/`: Contains malicious payloads attempting to exploit the legacy binary's flawed parsing logic.

You may use any programming language of your choice. Save your final classifier script as `/home/user/detector` and ensure it is executable. You can use standard reverse-engineering tools (like `strings`, `objdump`, or `gdb`) to analyze `/app/auth_redirector` and deduce the exact flaw in its URL parsing algorithm, ensuring your detector accurately blocks what the binary fails to catch.