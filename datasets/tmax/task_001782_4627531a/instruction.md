You are a compliance analyst tasked with generating an audit trail for a legacy authentication service that is currently being evaluated for deprecation. The source code for this legacy service has been lost, and all we have is the compiled executable and the legacy database.

Your task is to analyze the binary, crack a specific administrator's password, test the live authentication endpoint, and generate a compliance audit report.

Here are the details and assets provided to you:
1. **The Target Service:** An ELF binary located at `/home/user/legacy_auth.bin`. This binary is currently running as a background service and is listening for HTTP POST requests on `http://127.0.0.1:9090/login`.
2. **The Database:** A text file at `/home/user/db.txt` containing usernames and hashed passwords in the format `username:hash`. 
3. **The Target User:** You must audit the account for `compliance_admin`.
4. **The Wordlist:** A dictionary file is located at `/home/user/wordlist.txt`.

The legacy system uses SHA256 for hashing, but it appends a hardcoded, 16-character printable ASCII salt to the plaintext password before hashing (i.e., `SHA256(password + salt)`).

Perform the following steps:
1. **ELF Analysis:** Analyze `/home/user/legacy_auth.bin` to discover the hardcoded 16-character salt. 
2. **Password Cracking:** Write a C++ program named `/home/user/cracker.cpp` that reads `/home/user/wordlist.txt`, appends the discovered salt, computes the SHA-256 hash (using OpenSSL), and compares it against the hash for `compliance_admin` found in `/home/user/db.txt` to find the plaintext password. Compile and run it to recover the password.
3. **Authentication Flow Testing:** Send an HTTP POST request to `http://127.0.0.1:9090/login` with a JSON payload containing the recovered credentials: `{"username": "compliance_admin", "password": "<cracked_password>"}`. Note the HTTP status code and the exact text of the response body.
4. **Audit Trail Generation:** Create a JSON file at `/home/user/audit_trail.json` containing the results of your investigation. The JSON must have exactly the following keys and structure:
```json
{
  "salt": "<the 16-character salt extracted from the binary>",
  "cracked_password": "<the plaintext password of compliance_admin>",
  "auth_status_code": <integer HTTP status code from step 3>,
  "auth_response_body": "<exact string of the HTTP response body from step 3>"
}
```

Ensure all dependencies for your C++ program (like `libssl-dev`) are installed if not already present.