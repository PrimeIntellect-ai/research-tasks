You are a forensics analyst investigating a compromised Linux host. You have recovered an encrypted archive and a suspicious image file left behind by the attacker. Your goal is to extract the stolen evidence, verify its integrity, and stand up a secure staging server to securely hand off the evidence to the incident response (IR) team.

Here is your workflow:

1. **Evidence Extraction (Password Cracking & File Integrity):**
   - The attacker left an image file at `/app/evidence.png`. Use OCR (`tesseract`) to extract the text from this image. 
   - The text in the image is a partial password prefix. The actual password for the encrypted archive `/home/user/vault.zip` consists of this prefix followed by an underscore and a two-digit number (e.g., `PREFIX_00` to `PREFIX_99`).
   - Brute-force the zip archive to extract `secret_data.txt`.
   - Verify the integrity of `secret_data.txt`. Its SHA-256 hash must exactly match the hash provided in `/home/user/hash.txt`.

2. **Staging Server Setup (TLS Management):**
   - The IR team requires the data to be served over HTTPS.
   - Generate a self-signed TLS certificate (`cert.pem`) and private key (`key.pem`) for `localhost`.
   - Create an HTTPS web server listening on TCP port `8443`. You must use `socat` with OpenSSL and a Bash script to handle the requests.

3. **Authentication Bypass Analysis (Payload Decoding):**
   - The attacker used a vulnerable JWT implementation. The IR team's automated collection script will authenticate to your server using a forged JWT that exploits the "algorithm=none" vulnerability.
   - Your Bash web server handler must read incoming HTTP GET requests and extract the `Authorization: Bearer <token>` header.
   - The handler must decode the Base64-encoded JWT header and payload.
   - If the header specifies `"alg":"none"` (ignoring whitespace) AND the payload contains `"role":"admin"`, the server must respond with an `HTTP/1.1 200 OK` header followed by the exact contents of `secret_data.txt`.
   - If the token is missing, invalid, or does not meet the above criteria, respond with an `HTTP/1.1 401 Unauthorized` header.

Ensure your `socat` listener is running in the background and bound to `0.0.0.0:8443`. Write the request handler entirely in Bash. You may use standard utilities like `jq`, `base64`, `grep`, and `sed`.