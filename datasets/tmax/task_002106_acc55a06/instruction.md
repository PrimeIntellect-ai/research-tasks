You are a network engineer analyzing traffic to an internal authentication API. Your intrusion detection systems have flagged unusual activity, and you suspect that an attacker might have bypassed the authentication flow by exploiting an injection vulnerability while presenting a valid, but compromised, client certificate.

You have been provided with:
1. An API gateway access log: `/home/user/gateway_logs.json`
2. A directory containing the client certificates used in the requests: `/home/user/certs/`
3. The organization's Root CA certificate chain: `/home/user/ca-chain.pem`

The JSON log is an array of objects, where each object represents an authentication request. Each object has the following keys:
- `req_id`: A unique integer ID for the request.
- `client_cert_file`: The filename of the client certificate in the `/home/user/certs/` directory (e.g., `client_1.pem`).
- `payload`: A stringified JSON body containing the authentication credentials.
- `response_code`: The integer HTTP status code returned by the server.

Your objective is to write a Python script (`/home/user/analyze.py`) that analyzes the log and identifies compromised authentication flows. A request represents a **compromised session** if AND ONLY IF it meets **all** of the following conditions:
1. **Valid Certificate:** The client certificate specified in `client_cert_file` cryptographically verifies against the `/home/user/ca-chain.pem` root certificate. (You may use standard tools like `openssl verify` via Python's `subprocess` module to check this).
2. **Malicious Payload:** The `payload` field contains either an XSS or SQL Injection attempt. Specifically, search for the exact substring `<script>` OR the exact substring `' OR `.
3. **Successful Authentication:** The `response_code` is `200`.

Once you have identified the compromised `req_id`s, write them to a log file located at `/home/user/compromised_sessions.txt`. 
The file must contain exactly one `req_id` per line, sorted in ascending numerical order. Do not include any other text in this output file.