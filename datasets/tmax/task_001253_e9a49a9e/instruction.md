You are a compliance analyst tasked with securing a legacy audit trail system and building a secure proxy to generate compliance reports.

The system currently runs under `/app/services/` and consists of two main components:
1. `log-ingest` (runs on `127.0.0.1:5002`): A Flask service that stores audit logs in an SQLite database. It has a known SQL injection vulnerability in its `/search` endpoint, and the logs are stored using a proprietary weak encryption algorithm.
2. `legacy-auth`: A compiled Python module (`/app/services/legacy-auth/auth_token.pyc`) that generates the admin cookie required to export the raw logs.

Your objectives:
1. **Reverse Engineer Authentication & Encryption:** Analyze `/app/services/legacy-auth/auth_token.pyc` to understand how the admin session cookie is constructed and how the audit logs are encrypted. 
2. **Data Extraction & Decryption:** Use the reverse-engineered logic to generate a valid admin cookie. Send a GET request to `http://127.0.0.1:5002/export` with this cookie to retrieve the encrypted audit logs. Write a Python script `/home/user/decrypt_logs.py` that takes the encrypted JSON from the export and writes a decrypted JSON array to `/home/user/decrypted_logs.json`.
3. **Vulnerability Remediation:** Inspect `/app/services/log-ingest/app.py` and fix the SQL injection vulnerability in the `/search` endpoint. Ensure that standard input validation and parameterized queries are used. You must restart the service after fixing it.
4. **Secure Audit Proxy:** Create and run a new service, `secure-audit-proxy`, listening on `127.0.0.1:9000`. This proxy must:
   - Accept HTTP GET requests at `/compliance?id=<id>`.
   - Require an HTTP header: `Authorization: Bearer COMPLIANCE_SECURE_TOKEN`. Reject unauthorized requests with a 401 status code.
   - Securely query the patched `log-ingest` service to fetch the specific log entry for the given `<id>`, decrypt it on the fly using your reverse-engineered logic, and return it as a JSON object: `{"id": <id>, "action": "<decrypted_action>", "user": "<decrypted_user>"}`.

The services can be started by running `/app/start.sh`. Ensure your proxy service remains running in the background for verification.