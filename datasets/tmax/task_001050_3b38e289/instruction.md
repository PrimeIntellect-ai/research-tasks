You are a DevSecOps engineer responsible for enforcing policy as code in our internal environment. We need to implement a standalone, secure C++ HTTP middleware service that processes incoming data, redacts sensitive information, and encrypts the output.

Due to a recent pipeline failure, our configuration management system outputted the current security policy as an image file instead of text. You will find this image at `/app/policy_config.png`.

Your objectives are:
1. Extract the policy configuration from the image. Use `tesseract` to read `/app/policy_config.png`. The image contains three critical pieces of information:
   - REQUIRED_COOKIE: A specific cookie name and value that must be present in all incoming HTTP requests.
   - REDACT_WORD: A sensitive project code-name that must be redacted from any incoming request body (replace the word entirely with `[REDACTED]`).
   - AES_KEY: A 32-character hexadecimal string representing the AES-256-CBC encryption key.

2. Write a C++ HTTP server program at `/home/user/middleware.cpp`. The server must:
   - Listen on `127.0.0.1:8080`.
   - Parse incoming HTTP POST requests.
   - Inspect the HTTP headers and cookies. If the `Cookie:` header does not contain the exact REQUIRED_COOKIE extracted from the image, respond with a `403 Forbidden` status.
   - For authorized requests, read the HTTP POST body.
   - Scan the POST body and redact all occurrences of the REDACT_WORD.
   - Encrypt the redacted POST body using AES-256-CBC encryption via the OpenSSL library (`libcrypto`), using the AES_KEY extracted from the image. Use an initialization vector (IV) of exactly 16 null bytes (`0x00`).
   - The encrypted payload must be Base64-encoded.
   - Respond with a `200 OK` status, returning the Base64-encoded encrypted text as the HTTP response body.

3. Compile your C++ code. You may link against standard libraries and OpenSSL (`-lcrypto`). The resulting binary should be located at `/home/user/middleware`.

4. Start your service in the background so that it listens on `127.0.0.1:8080`.

Do not create any log files unless you need them for debugging. Ensure your service handles basic HTTP POST parsing correctly (reading headers up to `\r\n\r\n` and then reading the body).