You are a DevSecOps engineer tasked with enforcing policy as code and auditing a newly deployed microservice environment. We suspect that our previous authentication mechanisms were vulnerable to misconfigurations and that an attacker might have already probed our logs.

Your objective is to complete three security tasks. You must write Python scripts to accomplish them.

**Task 1: Privilege Escalation Auditing via JWT Forgery**
We found that a legacy endpoint accepts JSON Web Tokens (JWT) with the algorithm set to `none`. 
Write a Python script at `/home/user/forge_jwt.py` that generates a forged JWT. 
- The header must specify `"alg": "none"` and `"typ": "JWT"`.
- The payload must specify `"user": "admin"` and `"role": "superuser"`.
- The script must print *only* the raw forged JWT string to standard output. 
Note: Ensure the JWT is correctly Base64Url encoded and has the proper structure (Header.Payload.Signature), where the signature is empty.

**Task 2: Intrusion Detection Pattern Matching**
We need to find out if attackers have exploited the `alg=none` vulnerability. 
You are provided with an access log at `/home/user/access.log`. The log lines have the following format:
`[TIMESTAMP] IP_ADDRESS METHOD /endpoint "Bearer <JWT_TOKEN>"`

Write a Python script at `/home/user/detect_alg_none.py` that:
1. Parses the `/home/user/access.log` file.
2. Extracts the JWT token from each line.
3. Decodes the Base64Url-encoded header of the JWT.
4. Checks if the `alg` field in the header is set to `none` (case-insensitive: e.g., `none`, `None`, `NONE`).
5. Extracts the IP address of any request that used an `alg=none` token.
6. Writes the unique, flagged IP addresses to `/home/user/flagged_ips.txt`, with exactly one IP address per line.

**Task 3: Certificate Chain Validation**
Our internal PKI might have issued a malformed certificate chain.
You are provided with a PEM file at `/home/user/certs/server_chain.pem`. It contains exactly three certificates in this order: Leaf Certificate, Intermediate Certificate, Root Certificate.
Write a script at `/home/user/validate_cert.py` that programmatically verifies the cryptographic signatures of the chain (i.e., verifies the Leaf is signed by the Intermediate, and the Intermediate is signed by the Root). You may use the `cryptography` Python library (`pip install cryptography`).
- If the chain is completely cryptographically valid, write the word `VALID` to `/home/user/cert_status.txt`.
- If any signature is invalid, write the word `INVALID` to `/home/user/cert_status.txt`.

Ensure all output files are placed exactly where specified.