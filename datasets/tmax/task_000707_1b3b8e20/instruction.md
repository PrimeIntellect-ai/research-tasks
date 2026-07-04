You are a compliance analyst responsible for securing a custom internal web server and generating a remediation audit trail.

The source code for the server is located at `/home/user/src/server.cpp`. It relies on the `cpp-httplib` header (located at `/home/user/src/httplib.h`) and uses SQLite for the database (`/home/user/data/users.db`). The server is intended to run on port `8080`.

Your security scan has flagged several critical vulnerabilities in `server.cpp`:
1. **Authentication Flow & Cryptography**: The `/login` endpoint currently verifies passwords using a weak custom checksum. The SQLite database actually stores SHA-256 hashes of the passwords. Update the login logic to hash the incoming password using SHA-256 (via OpenSSL) and compare it against the database hash.
2. **SQL Injection**: The `/login` endpoint constructs SQL queries by directly concatenating user input. Refactor the database query to use SQLite prepared statements (`sqlite3_prepare_v2`, `sqlite3_bind_text`, etc.) to prevent SQL injection.
3. **HTTP Headers & Cookies**: Upon successful login, the server sets a `session_id` cookie. This cookie is missing security attributes. Modify the `Set-Cookie` header to include the `HttpOnly` and `Secure` flags.
4. **Reflected XSS**: The `/greet` endpoint takes a `name` query parameter and reflects it directly in the HTML response. Implement a simple HTML entity encoding function (converting `<`, `>`, `&`, `"`, `'` to their respective HTML entities) and apply it to the `name` parameter before reflecting it.

**Your objectives:**
1. Install any necessary dependencies (e.g., `libssl-dev`, `libsqlite3-dev`, `g++`).
2. Fix the vulnerabilities in `/home/user/src/server.cpp` according to the requirements above.
3. Compile the fixed server to `/home/user/server_fixed`. Use the following compilation flags: `-std=c++11 -lsqlite3 -lssl -lcrypto -lpthread`.
4. Start the server in the background on port `8080`.
5. Generate an audit trail file at `/home/user/audit_trail.json` with the following exact structure:
```json
{
  "vulnerabilities_fixed": [
    "SQL_Injection",
    "Reflected_XSS",
    "Insecure_Cookie",
    "Weak_Password_Hashing"
  ],
  "hashing_algorithm_implemented": "SHA-256",
  "cookie_flags_added": ["HttpOnly", "Secure"]
}
```

Ensure the server is running and accessible on `http://127.0.0.1:8080` before finishing.