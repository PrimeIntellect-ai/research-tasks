You are an incident responder investigating a series of breaches. The attackers have compromised our proprietary authentication service. The service is a C program that validates custom JSON Web Tokens (JWTs) for user sessions. We have obtained a stripped copy of the vulnerable daemon binary, located at `/app/auth_daemon`.

Initial analysis suggests the attackers are exploiting multiple flaws to escalate privileges:
1. The token parser accepts tokens with `alg` set to `none` (bypassing signature checks).
2. The service uses a hardcoded, weak HMAC-SHA256 secret key embedded in the binary, which the attackers have extracted to forge tokens with elevated privileges (e.g., `"role":"admin"`).

We have captured a dataset of tokens. Some are legitimate, and some are forged or malicious.
You must build a token filter to identify and reject malicious tokens.

Your tasks:
1. Analyze the `/app/auth_daemon` binary to recover the hardcoded HMAC-SHA256 secret key.
2. Write a C program at `/home/user/detector.c` and compile it to `/home/user/detector`.
3. The program must accept exactly one command-line argument: the path to a file containing a single JWT string.
4. The program must parse and validate the token, exiting with code `0` if the token is legitimate (clean) and code `1` if the token is malicious (evil) or malformed.

A token is considered **MALICIOUS (exit code 1)** if ANY of the following are true:
- The header specifies `"alg":"none"` (or any case variation of "none").
- The token payload contains `"role":"admin"`.
- The token has an invalid signature (unless it was already flagged for `alg=none`).

A token is considered **LEGITIMATE (exit code 0)** if:
- It uses `"alg":"HS256"`.
- It has a valid HMAC-SHA256 signature using the secret key extracted from the binary.
- Its payload does not contain the admin role (e.g., `"role":"user"`).

Notes:
- You may use OpenSSL (`libcrypto`) or other standard C libraries for Base64Url decoding and HMAC-SHA256 calculation.
- Compile your program with `gcc -o /home/user/detector /home/user/detector.c -lcrypto`.
- Ensure your program gracefully handles missing files, malformed tokens, or invalid Base64Url encoding by exiting with code `1`.