You are a security auditor tasked with fixing data leaks in a multi-service application. The system serves compiled binaries to users and logs the access, but it currently leaks sensitive information in two ways:
1. The ELF binaries themselves contain hardcoded email addresses in their `.rodata` sections.
2. The access logs contain plaintext user email addresses.

The application consists of the following internal services running on localhost:
- **Binary Service** (`http://localhost:8001`): Has an endpoint `/fetch?id=<binary_id>`. It returns a JSON response: `{"id": "<binary_id>", "payload": "<base64_encoded_elf_binary>"}`.
- **Log Service** (`http://localhost:8002`): Accepts `POST` requests at `/log` with a JSON body to record access events.

Your task is to write and run a secure Python proxy service at `/home/user/proxy.py` that listens on `0.0.0.0:8000` using Flask or standard library `http.server`. 

When a client makes a `GET` request to your proxy at `http://localhost:8000/download?id=<binary_id>&user=<user_email>`, your proxy must:
1. Fetch the corresponding binary from the Binary Service.
2. Decode the base64 payload to get the raw ELF binary.
3. Parse the ELF structure to locate the `.rodata` section.
4. Find any ASCII email addresses within the `.rodata` section and redact them by replacing every character of the email address with an asterisk (`*`). You must do this in-place so the length of the string remains exactly the same, ensuring the ELF file offsets are not corrupted and the file remains a valid, executable ELF.
5. Re-encode the redacted ELF binary as base64.
6. Redact the user's email address for logging by hashing it using HMAC-SHA256 with the secret key `AUDIT_KEY`.
7. Send a `POST` request to the Log Service at `http://localhost:8002/log` with the JSON body: `{"id": "<binary_id>", "user_hash": "<hex_digest_of_hmac>"}`.
8. Return an HTTP 200 JSON response to the client: `{"id": "<binary_id>", "payload": "<redacted_base64_encoded_elf_binary>"}`.

Requirements:
- Do not corrupt the ELF headers or other sections. The resulting binary must still be perfectly parseable by tools like `readelf`.
- Redact *only* valid email addresses in the `.rodata` section.
- Keep your proxy running in the background when you are done, so the automated test suite can exercise it. 

Start the internal services by running `/app/start_services.sh` before you begin testing.