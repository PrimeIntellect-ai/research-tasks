You are a security engineer assigned to handle a credential rotation incident. We have recently rotated our JWT signing keys due to a potential leak. However, our API logs from the transition period contain a mix of requests authenticated with the old compromised key, requests using the new key, and some maliciously forged tokens. Furthermore, the logging system was inadvertently recording the full Bearer tokens in plaintext, which is a CWE-312 vulnerability (Cleartext Storage of Sensitive Information).

Your task is to audit and sanitize these logs.

1. **Fix and Install the Vendored Library**:
   We use a specific version of `PyJWT` for our authentication flow testing. The source code is pre-vendored at `/app/pyjwt-2.8.0`. Unfortunately, an automated tool corrupted its build configuration, and you cannot install it directly via pip from the directory. Identify the perturbation in the package configuration files, fix it, and install the library in your environment. NO INTERNET access is available.

2. **Audit and Redact Logs**:
   You have been provided with an API log file at `/home/user/api_requests.log`. Each line contains a JSON object representing an HTTP request, including an `Authorization` header with a Bearer token.
   
   - **Old (Compromised) Key:** `legacy_secret_992`
   - **New Key:** `rotated_secure_key_2024`
   - **Algorithm:** `HS256`

   Write a Python script to process `/home/user/api_requests.log`.
   For each line:
   - Extract the JWT from the `Authorization` header.
   - Attempt to verify the token signature. 
   - If the token is valid and signed with the **New Key**, write the *entire original JSON line* to `/home/user/valid_requests.log`.
   - If the token is signed with the **Old Key**, or the signature is completely invalid/forged, you must redact the sensitive token to mitigate the CWE-312 violation. Replace the token string in the JSON with exactly the string `[REDACTED_CWE312]` and write the modified JSON line to `/home/user/invalid_requests.log`.

Your script's output will be evaluated automatically. The grading script will compute the classification and redaction accuracy. You must achieve an accuracy score of >= 0.99.