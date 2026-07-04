You are an incident responder investigating a compromised Linux bastion host. The attacker has modified SSH configurations, planted persistent keys, and dropped a custom C binary used to validate backdoor access tokens via X.509 certificate chains.

Your objective is to audit the system, find the persistence mechanisms, and reverse-engineer/fix the attacker's token validator to identify which dropped token is the active backdoor.

**Phase 1: SSH Audit**
1. Inspect the SSH configuration file located at `/home/user/investigation/sshd_config`. The attacker added a secondary, non-standard hidden port for backdoor access. Identify this backdoor port and write the port number (just the digits) to `/home/user/audit_port.txt`.
2. Inspect the authorized keys file at `/home/user/investigation/authorized_keys`. The attacker planted a deprecated, cryptographically weak key type (`ssh-dss`). Identify the comment field of this specific key and write the comment string to `/home/user/audit_key.txt`.

**Phase 2: Token Validator Code Review & Fix**
The attacker left behind the source code for their custom token validator at `/home/user/investigation/validator.c`. This program is meant to read a certificate (`.pem`) file passed as an argument, and validate its chain against a hardcoded Trust Anchor (`/home/user/investigation/ca.pem`). 

However, the attacker made a critical flaw in the C code: the verification logic is broken, causing it to successfully "validate" *any* loaded certificate, even self-signed ones not chained to the CA.

1. Review `/home/user/investigation/validator.c`.
2. Find the OpenSSL `X509_verify_cert` function call. Read the OpenSSL documentation (or use your knowledge) to understand its return values.
3. Fix the logic flaw so the program correctly prints "VALID" and exits with code `0` ONLY if the certificate chain is cryptographically valid and signed by `ca.pem`. For any invalid certificate, it must print "INVALID" and exit with code `1`.
4. Recompile the fixed code:
   `gcc /home/user/investigation/validator.c -o /home/user/investigation/validator -lssl -lcrypto`

**Phase 3: Active Token Identification**
The attacker left three candidate token certificates in `/home/user/investigation/tokens/`:
- `token_alpha.pem`
- `token_beta.pem`
- `token_gamma.pem`

1. Use your fixed, compiled `/home/user/investigation/validator` to test all three tokens.
2. Only one of these tokens is actually signed by the attacker's CA. Identify the filename of the valid token.
3. Write the exact filename (e.g., `token_alpha.pem`) to `/home/user/valid_token_file.txt`.