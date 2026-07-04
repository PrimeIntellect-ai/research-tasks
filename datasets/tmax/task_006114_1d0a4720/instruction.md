You are a network engineer analyzing suspected malicious traffic. You have intercepted a log of encrypted HTTP requests sent to an internal file upload service. You suspect one of the requests contains a path traversal attack disguised within the file upload payload.

Your task is to write a Go program that decrypts the traffic logs, analyzes the HTTP payloads to identify the path traversal attack, and extracts the attacker's details to block them.

Here are the details of the environment:
1. The 256-bit encryption key is stored as a hex-encoded string in `/home/user/key.txt`.
2. The encrypted traffic logs are in `/home/user/traffic.json`. Each line is a JSON object with the following structure:
   `{"ip": "192.168.X.X", "ciphertext": "<hex-encoded-data>"}`
3. The `ciphertext` is encrypted using AES-256-GCM. The first 12 bytes of the decoded binary data represent the GCM nonce, and the remainder is the actual encrypted payload (which includes the authentication tag at the end, as standard in Go's `crypto/cipher` GCM implementation).
4. Upon decryption, the payload is a raw string of an HTTP POST request.
5. One of these HTTP requests is a multipart file upload containing a path traversal payload in the `filename` parameter of the `Content-Disposition` header (e.g., trying to escape the upload directory using `../`).

Using Go, write a script to:
1. Decrypt all payloads in `/home/user/traffic.json`.
2. Inspect the decrypted HTTP POST requests to find the path traversal attack in the `filename` attribute.
3. Once identified, extract the IP address of the attacker and save it to `/home/user/blocked_ip.txt`.
4. Extract the exact malicious string used in the `filename` attribute and save it to `/home/user/malicious_filename.txt`.

Ensure your Go script handles the decryption properly and correctly parses the HTTP headers to find the vulnerability. Only save the requested information into the two output files. No extra formatting should be present in the output files (just the raw string/IP).