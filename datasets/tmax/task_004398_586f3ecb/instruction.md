You are a security engineer tasked with rotating credentials for a legacy authentication microservice. You need to write a new validation service in C++ that uses a newly issued master key and a legacy salt to validate incoming security tokens.

Perform the following steps:

1. **Recover the New Master Key:**
   A physical recovery card was scanned and saved at `/app/new_master_key.png`. Use an OCR tool (like `tesseract`) to read the text from this image. The image contains a single string of text, which is the new master key.

2. **Extract the Legacy Salt:**
   The legacy authentication salt is embedded inside a compiled binary located at `/app/legacy_crypto.so`. You must perform ELF analysis to extract the raw string from a custom section named `.secret_salt`. Do not include any null terminators in the extracted salt string.

3. **Develop the Validation Service (C++):**
   Write a C++ HTTP server (you may use a single-header library like `cpp-httplib` which you can download) that listens on `127.0.0.1:8080`.
   The server must implement a single endpoint:
   - **Method:** `POST`
   - **Path:** `/verify`
   - **Content-Type:** `application/json`
   - **Request Body Format:** `{"token": "<custom_token>"}`

   The `<custom_token>` is formatted as `payload_hex.hmac_hex`.
   - `payload_hex` is the hex-encoded string of the token data.
   - `hmac_hex` is the hex-encoded HMAC-SHA256 signature of the *decoded* payload string.

   **Validation Logic:**
   - The key for the HMAC-SHA256 must be exactly the concatenation of the OCR master key and the ELF salt, separated by a colon: `<master_key>:<elf_salt>`.
   - Ensure the OCR text is stripped of any trailing newlines or whitespace before concatenation.
   - Compute the HMAC-SHA256 of the decoded payload.
   - If the computed HMAC matches the provided `hmac_hex`, respond with HTTP status `200` and JSON `{"status": "success"}`.
   - If it does not match or the token is malformed, respond with HTTP status `401` and JSON `{"status": "failed"}`.

4. **Deploy:**
   Compile your C++ service (ensure you link OpenSSL for HMAC calculations, e.g., `-lcrypto`) and run it in the background so it is actively listening on `127.0.0.1:8080` when your final response is submitted.