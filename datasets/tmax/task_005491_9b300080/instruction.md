You are a compliance analyst generating an audit trail for a legacy web application. We suspect an attacker has bypassed authentication. You have been provided with an HTTP request log and the custom authentication daemon (an ELF binary) from the server.

Your task is to write a C++ program at `/home/user/analyzer.cpp` that performs a full analysis of the logs, identifies forged tokens, verifies legitimate tokens, and cracks a compromised user PIN. 

**Available Files:**
1. `/home/user/audit_data/requests.log`: Raw HTTP request logs. Each request is separated by a blank line. Tokens are passed in the `Cookie` header as `session_token=<JWT>`.
2. `/home/user/audit_data/auth_daemon`: The legacy compiled ELF authentication service.

**Objectives & Workflow:**
1. **ELF Analysis:** The `auth_daemon` binary contains the hardcoded secret key used to sign legitimate JWTs. Analyze the binary to find this secret. The key is stored in the read-only data section as a null-terminated string that begins exactly with the prefix `KEY_MATERIAL_`. The actual secret is the string immediately following this prefix.
2. **HTTP & Payload Inspection:** Parse `requests.log` to extract all `session_token` JWTs. A JWT consists of three Base64Url-encoded parts: Header, Payload, and Signature. Decode the Headers and Payloads.
3. **Vulnerability Detection:** Identify any JWTs that exploit the "None algorithm" bypass. These are tokens where the Header's `alg` field is set to `none` (case-insensitive). Count how many such forged requests exist in the log.
4. **Password Cracking:** Find the legitimate admin tokens. A legitimate token is one where `alg` is `HS256`, the signature is valid (using the HMAC-SHA256 of the secret extracted from the ELF), and the Payload contains `"user": "admin"`. 
   The payload of legitimate admin tokens also contains a `"pin_hash"` field, which is the MD5 hash of the admin's 4-digit numerical PIN (e.g., `0000` to `9999`). You must brute-force this hash to find the original 4-digit PIN.

**Output Specification:**
Your C++ program (`analyzer.cpp`) must compile using `g++` (you may use OpenSSL for crypto functions, e.g., `-lcrypto`) and output its final results to `/home/user/report.txt`. 

The file `/home/user/report.txt` must contain exactly three lines:
Line 1: The extracted secret key (just the secret part, without the `KEY_MATERIAL_` prefix).
Line 2: The total number of requests containing forged JWTs (`alg` = none).
Line 3: The 4-digit admin PIN.

*Note: Do not use external libraries other than the standard C++ library and OpenSSL (which is already installed on the system). Shell commands like `strings`, `objdump`, or `grep` are permitted for manual analysis, but the primary logic (parsing, decoding, cracking) must be executed by your C++ program.*