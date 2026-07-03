You are a compliance analyst auditing an internal microservice. You have been provided with access logs, a wordlist, and the server's TLS certificate. Your goal is to identify security vulnerabilities related to JWT authentication bypass, weak signing secrets, and certificate misconfigurations, and then generate an audit trail.

You have the following files in your home directory (`/home/user/`):
1. `requests.json`: A JSON file containing an array of HTTP request logs. Each entry has an `"ip"`, `"method"`, `"path"`, and an `"authorization"` header (containing a Bearer JWT).
2. `wordlist.txt`: A list of common passwords.
3. `server.crt`: The X.509 TLS certificate used by the microservice.

Perform the following tasks:
1. **JWT Vulnerability Scanning (alg=none):** Parse the `requests.json` file. Identify any JWT that is attempting an `alg=none` (or `None`, `NONE`) signature bypass. Extract the `"username"` claim from the payload of this malicious token.
2. **JWT Secret Cracking:** The microservice uses `HS256` for valid tokens. Extract the valid `HS256` tokens from the logs. Write a Python script to brute-force the HMAC-SHA256 secret using the passwords provided in `wordlist.txt`. Find the secret key used to sign the valid tokens. 
3. **TLS Certificate Auditing:** Inspect the `server.crt` file and extract the Common Name (CN) of the certificate's Issuer.

Once you have gathered this information, create an audit report at `/home/user/audit_trail.txt` with exactly the following format (one key-value pair per line, separated by a colon, no spaces around the colon):

```
CRACKED_SECRET:<the_cracked_jwt_secret>
ALG_NONE_USER:<username_from_alg_none_token>
CERT_ISSUER:<issuer_common_name>
```

Ensure your Python scripts and shell commands do not require root access.