You are a security engineer tasked with rotating credentials for an internal database after a suspected leak. The legacy credential rotation system was found to be insecure.

Your objective has four phases:

1. **Legacy Key Recovery (Image Analysis & Brute-Force):**
   The base of the legacy master key was written on a physical sticky note, a photo of which is stored at `/app/legacy_key.png`. Recover the text from this image. The security team knows this base text is missing a 2-character lowercase alphabetic suffix (e.g., `aa`, `ab`, ..., `zz`).
   There is an encrypted backup file at `/app/db_backup.enc` containing the actual database credentials. It was encrypted using AES-256-GCM. The encryption key is the SHA-256 hash of the complete legacy master key (the base from the image + the 2-character suffix). The initialization vector (IV) used was `000000000000000000000000` (12 bytes of zeros).
   Brute-force the suffix, decrypt the backup, and extract the JSON contents. Write the completely recovered legacy master key to `/app/recovered_key.txt`.

2. **Vulnerability Analysis:**
   Analyze the legacy shell script located at `/app/old_service.sh`. It was used to launch the database client but leaked credentials to unprivileged users monitoring system state. Identify the specific CWE (Common Weakness Enumeration) identifier that best describes this vulnerability (e.g., CWE-XXX). Write ONLY the exact CWE identifier (e.g., "CWE-123") to a file named `/app/audit.txt`.

3. **Secure Credential Rotation Service (Rust):**
   Create a new secure HTTP service in Rust to handle future credential rotations. Initialize a Rust project in `/app/rotation_service` and run the service.
   The service must:
   - Listen on exactly `127.0.0.1:8080`.
   - Expose an HTTP POST endpoint at `/rotate`.
   - Require an `Authorization: Bearer <LEGACY_MASTER_KEY>` header to authenticate the request (using the fully recovered key from phase 1).
   - Accept a JSON body containing `{"new_key": "<string>"}`.
   - Upon receiving a valid request, the service must take the raw, decrypted JSON database credentials (from phase 1), re-encrypt them using AES-256-GCM where the encryption key is the SHA-256 hash of the provided `new_key`, and the IV is exactly `111111111111111111111111` (12 bytes of ones, hex-encoded: `313131313131313131313131`).
   - The endpoint must return the base64-encoded ciphertext (appended with the GCM authentication tag as the last 16 bytes of the ciphertext buffer) in a JSON response: `{"encrypted_credentials": "<base64_string>"}`.
   - Return a `401 Unauthorized` status code if the Bearer token is missing or incorrect.

4. **Deployment:**
   Leave the Rust service running in the background.

Use standard Linux tools (e.g., `tesseract` for OCR) and write custom Rust code where necessary. Ensure your Rust service compiles and binds to the correct port.