You are an incident responder investigating a compromised web server. The attackers exploited an open redirect vulnerability in the login flow to steal user tokens. They also left a taunting image file on the server.

Your task is to analyze the evidence, secure the environment, and deploy a patched, secure version of the login service.

Perform the following steps:

1. **Evidence Analysis:**
   - There is an image file left by the attacker at `/app/evidence.png`.
   - Use OCR (e.g., `tesseract`) to extract the text from this image. It contains the attacker's exfiltration domain in the format `ATTACKER_DOMAIN: <domain>`. You will need this domain to write specific intrusion detection rules.

2. **TLS/SSL Certificate Management & File Permissions:**
   - Create a directory `/app/certs/`.
   - Generate a self-signed RSA-2048 certificate (`server.crt`) and private key (`server.key`) valid for 365 days. 
   - Ensure the subject of the certificate is `CN=localhost`.
   - To prevent privilege escalation and unauthorized access, secure the private key: the file `/app/certs/server.key` MUST have exactly `600` permissions.

3. **Secure Web Service Implementation (Python):**
   - Write a Python web server at `/app/server.py` that listens on HTTPS (using your generated certificates).
   - **Host:** `127.0.0.1`
   - **Port:** `8443`
   - Implement a single endpoint: `GET /login`
   - The `/login` endpoint takes a `next` query parameter (e.g., `/login?next=/dashboard`).
   - **Security Rules (Pattern Matching):**
     - If the `next` parameter contains the specific attacker domain extracted from the image, return a `403 Forbidden` response with the text `Intrusion Detected`.
     - If the `next` parameter is an absolute URL (e.g., starts with `http://` or `https://` or `//`), indicating a potential open redirect to *any* external site, return a `400 Bad Request` with the text `Invalid Redirect`.
     - If the `next` parameter is a valid relative path (e.g., `/dashboard` or `/settings`), return a `302 Found` with the `Location` header set to the value of `next`.
   - Start the server in the background so it is actively listening when you finish. Write its PID to `/app/server.pid`.

Ensure your server remains running and listening on `127.0.0.1:8443` over HTTPS.