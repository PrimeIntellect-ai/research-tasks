You are a network security engineer tasked with implementing a high-performance, C-based security filter for a legacy microservice architecture. 

Currently, our system has a vulnerable backend service listening on `127.0.0.1:8081`. We have a traffic generator that simulates incoming traffic on `127.0.0.1:8080`. 
Your task is to write a C-based reverse proxy that binds to `127.0.0.1:8080`, inspects incoming HTTP traffic, and securely forwards valid requests to the backend at `127.0.0.1:8081`. The proxy must drop invalid or malicious requests by returning an HTTP `403 Forbidden` response.

The authentication mechanism uses a custom encrypted cookie named `SecureSession`. 
Here are the specifications for the traffic and the security filter:

1. **HTTP Header & Cookie Inspection**:
   - Parse incoming HTTP/1.1 GET requests.
   - Extract the `SecureSession` cookie from the `Cookie` header.

2. **Encryption & Decryption**:
   - The `SecureSession` cookie value is a hex-encoded string.
   - When decoded from hex, the first 16 bytes represent the Initialization Vector (IV).
   - The remainder of the bytes represent the ciphertext.
   - The ciphertext is encrypted using AES-128-CBC. 
   - The symmetric key is exactly 16 bytes: `S3cr3tK3y1234567` (ASCII).
   - You must use OpenSSL (`libcrypto`) to decrypt the cookie.

3. **Authentication Flow & Validation**:
   - The decrypted plaintext (padded with PKCS#7) is a pipe-separated string in the format: `user_id|role|timestamp`.
   - You must block (return HTTP 403) ANY request that meets one of the following criteria:
     a) The `SecureSession` cookie is missing.
     b) The cookie fails to decrypt correctly or has an invalid format.
     c) The `role` is exactly `admin` AND the `user_id` is NOT exactly `1000`.
     d) The `timestamp` (a UNIX epoch integer) is strictly greater than `1800000000` (which we consider an invalid future token for this scenario).
   - Valid requests must be forwarded as-is to `127.0.0.1:8081`, and the proxy must return the backend's response back to the client.

**Requirements:**
- Write your C proxy in `/home/user/proxy.c` and compile it to `/home/user/proxy`. 
- Ensure your proxy is robust enough to handle multiple connections (you may use standard single-threaded non-blocking I/O, `select`/`poll`, or `fork`/`pthread` as you see fit).
- The proxy must be running when verification occurs.
- You must achieve an accuracy threshold of at least 98% (Accuracy >= 0.98) when our automated traffic generator evaluates your proxy against a mix of valid, forged, and malicious requests.

Please write, compile, and run the proxy in the background before declaring completion.