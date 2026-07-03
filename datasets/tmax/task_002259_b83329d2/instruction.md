You are a forensics analyst recovering evidence from a compromised Linux host. The attacker deployed a malicious ELF binary to encrypt critical evidence logs and disabled the internal log recovery API. 

Your objective is to fix the internal Rust-based recovery API, connect it to the backend storage service, extract the attacker's encryption key from their malware, and bring the API online so the automated forensics extraction tool can recover the logs.

Here is the current state of the system in `/app/`:
1. `/app/storage_backend.py`: A Python service that serves encrypted evidence logs over HTTP on `127.0.0.1:9000`. You must ensure this service is running.
2. `/app/malware_implant.bin`: The attacker's compiled ELF binary. The attacker embedded a 64-character hex string (representing a SHA256 hash used as the AES-256 decryption key) inside the `.rodata` section of this binary.
3. `/app/recovery_api/`: A Rust web service (using `axum` or `actix-web`) meant to retrieve, decrypt, and export evidence. 

Your tasks:
1. **ELF Analysis & Cryptography:** Analyze `/app/malware_implant.bin` to extract the 64-character hex string from its `.rodata` section. 
2. **Code Auditing (CWE Identification):** Audit the Rust application in `/app/recovery_api/`. 
   - Update the hardcoded dummy key in the decryption function with the actual hex string you extracted from the malware.
   - The API contains a Severe Path Traversal vulnerability (CWE-22) in the `/export` endpoint (which saves logs to disk). Fix the endpoint logic so that it strictly prevents path traversal and only writes files into the `/app/recovery_api/exports/` directory. Disallow any filenames containing `..` or `/`.
   - The API is currently failing to verify the cryptographic checksum of the downloaded encrypted evidence. Implement a SHA256 hash check in the Rust code: the SHA256 hash of the *decrypted* evidence must match the `X-Checksum` header provided by the storage backend. If it does not match, the API must return an HTTP 500 error.
3. **Multi-Service Composition:** Update the `/app/recovery_api/.env` file to correctly point `STORAGE_URL` to the Python storage backend (`http://127.0.0.1:9000`).
4. **Deployment:** Compile and run the fixed Rust API service. It must listen on `127.0.0.1:8080`.

Ensure both the Python storage backend and the Rust recovery API are running continuously in the background when you complete your turn. Our automated verifier will make HTTP requests to your Rust API (`127.0.0.1:8080`) to test the protocol flow, evidence decryption, and the CWE-22 mitigation.