You are a security engineer tasked with rotating credentials and updating security configurations for an internal application. You have received an encoded data package containing the old application environment.

Perform the following tasks in the terminal:

**Phase 1: Payload Decoding and Integrity Verification**
1. You will find a base64-encoded file at `/home/user/incoming_data.b64`. Decode this file into a compressed archive at `/home/user/archive.tar.gz`.
2. Verify the SHA256 checksum of `/home/user/archive.tar.gz`. Write a log file at `/home/user/integrity.log` containing exactly the word `PASS` if the extraction is successful and you are ready to proceed.
3. Extract the archive into `/home/user/app_data/`.

**Phase 2: TLS/SSL Certificate Management**
The extracted archive contains an expiring certificate. You must rotate it.
1. Generate a new RSA 2048-bit private key saved exactly to `/home/user/app_data/new_key.pem`.
2. Generate a new self-signed X.509 certificate valid for 365 days saved exactly to `/home/user/app_data/new_cert.pem`.
3. The certificate's Subject must contain exactly the Common Name (CN): `secure.internal`.

**Phase 3: Network Policy Configuration**
The extracted archive contains a file `allowed_ips.txt`. 
1. Read this file.
2. Write a script in any language (or use shell tools) to process these IPs and generate a JSON firewall policy file at `/home/user/firewall_policy.json`.
3. The JSON file must have exactly this structure:
```json
{
  "inbound_allow": ["<ip1>", "<ip2>", "..."],
  "default_action": "deny"
}
```

**Phase 4: Vulnerability Scanning & Credential Rotation**
The extracted archive contains a source file `app.py`.
1. Scan `app.py` to identify the hardcoded credential variable named `SECRET_TOKEN`.
2. Replace the hardcoded plaintext value in `app.py` with the base64-encoded string of the word `rotated_secure_token_999`. Do not change the variable name, only its assigned string value.

Make sure all files are saved in the exact paths specified above.