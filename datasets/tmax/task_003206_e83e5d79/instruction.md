You are a network security engineer investigating a recent breach. Attackers exploited an open redirect vulnerability in the company's legacy login flow, bypassing network restrictions. Your goal is to secure the application architecture, reverse engineer the weak cryptographic token mechanism, and build a robust filter to block malicious redirects.

The application infrastructure is located in `/app/` and consists of multiple services:
1. An Nginx reverse proxy listening on port `8443` (SSL termination).
2. A Flask login backend running on port `5000`.
3. A legacy Python bytecode tool (`/app/bin/token_generator.pyc`) used by other internal systems to generate redirect tokens.

**Phase 1: Multi-Service Configuration (Certificate Chain Validation)**
The Nginx reverse proxy is currently misconfigured and allows any client to connect. You must update `/app/nginx/nginx.conf` so that it strictly enforces Mutual TLS (mTLS).
- It must validate client certificates against the Certificate Authority located at `/app/certs/ca.crt`.
- If a client does not provide a valid certificate signed by this CA, Nginx must reject the connection.
- Valid requests must be forwarded to the Flask app on `127.0.0.1:5000`.
- Once configured, ensure the services are running. You can start/restart them using the provided `/app/start_services.sh` script.

**Phase 2: Cryptanalysis & Reverse Engineering**
The login system accepts a `token` parameter, which is a cryptographically manipulated string intended to securely encode the redirect URL. However, the implementation is custom and deeply flawed.
- Analyze the compiled Python 3.10 bytecode file `/app/bin/token_generator.pyc`.
- Reverse engineer its logic to determine the secret key and the algorithm (a weak cipher) used to encode the URLs.
- You do not have the original source code, so you must use disassembly or decompilation techniques (e.g., standard Python `dis` module).

**Phase 3: Adversarial Corpus & Filter Creation**
We have captured a corpus of both legitimate redirect tokens and malicious attacker tokens.
- **Clean Corpus:** `/app/corpus/clean/` (Contains files, each with a single token string representing a redirect to our internal domain `https://internal.corp.local/`).
- **Evil Corpus:** `/app/corpus/evil/` (Contains files with tokens that represent open redirects to external domains like `http://evil.attacker.com/`, or tokens with invalid cryptography).

You must write a Python script at `/home/user/filter.py` that takes a file path as its first positional argument.
The script must:
1. Read the token from the file.
2. Decrypt/decode the token using the algorithm and key you reverse-engineered.
3. Validate the destination URL.
4. Exit with code `0` ONLY if the token successfully decrypts AND the resulting URL starts exactly with `https://internal.corp.local/`.
5. Exit with code `1` if decryption fails, the structure is invalid, or the URL points anywhere else.

**Phase 4: Integration**
Finally, integrate your filter into the Flask application.
- Edit `/app/flask/app.py`.
- Locate the `/login` endpoint. Before returning the redirect response, the Flask app must use the `subprocess` module to call `/home/user/filter.py` with a temporary file containing the requested token.
- If the filter returns exit code `0`, proceed with the redirect.
- If the filter returns exit code `1`, return a `403 Forbidden` HTTP response.

Ensure your Nginx configuration is valid and both services are running smoothly before completing your task.