You are an incident responder investigating a severe authentication bypass incident affecting our internal microservices. 

Recently, attackers have been able to access internal administrative endpoints without valid credentials. All internal services use a custom-vendored version of the PyJWT library for token validation, located at `/app/pyjwt-vendored/`.

We suspect an insider threat maliciously modified this vendored package to introduce a backdoor that allows signature verification bypass under specific payload encoding conditions.

Your task:
1. Audit the vendored PyJWT library source code at `/app/pyjwt-vendored/` to identify the malicious backdoor related to token generation and validation.
2. Patch the vulnerability in the vendored library to restore proper security invariants (ensuring forged tokens are rejected).
3. To confirm your understanding of the exploit, write a Python script at `/home/user/scanner.py` that:
   - Scans localhost ports 8000 through 8010 to find running HTTP services.
   - For each active service, crafts a malicious JWT payload using the vulnerability you found (encoded to grant the payload `{"user": "attacker", "role": "admin"}`).
   - Sends a `GET /admin` request with the crafted token in the `Authorization: Bearer <token>` header.
   - Logs the ports of the vulnerable services to `/home/user/vulnerable_ports.txt` (one port per line).

You have full access to the source code of the vendored package. Once you fix the package, an automated test suite will evaluate the accuracy of your patched library against a large corpus of valid, invalid, and forged tokens.