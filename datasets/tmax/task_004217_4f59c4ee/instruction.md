You are tasked with building a secure auditing proxy and service endpoint in Rust to help evaluate vulnerability scanners.

First, you will find an image file located at `/app/target_info.png`. This image contains a secret authentication token (printed in plain text). Extract this token (you may use `tesseract` which is installed on the system). Remove any trailing whitespace from the extracted token.

Second, initialize a Rust project in `/home/user/audit_service` and write a server that listens on two different ports simultaneously, handling different protocols. You may use standard library `std::net` or any lightweight crates if you set up the `Cargo.toml` properly (e.g., standard `std::net::TcpListener` is sufficient and encouraged for simplicity).

**1. HTTP Service (Port 8080):**
Listen on `127.0.0.1:8080` for HTTP/1.1 requests.
- All responses must include the Content Security Policy header: `Content-Security-Policy: default-src 'none'; frame-ancestors 'none';`
- If the request is a `POST` to `/audit`, you must inspect the HTTP headers. The request must include an `Authorization` header in the format `Bearer <TOKEN>`, where `<TOKEN>` is the secret extracted from the image.
  - If the token is missing or incorrect, respond with `HTTP/1.1 401 Unauthorized`.
  - If the token is correct, read the body of the request, compute its SHA256 cryptographic hash (in lowercase hex), and respond with `HTTP/1.1 200 OK` including the header `X-Body-Hash: <sha256_hex_of_body>`.
- For any other path or method, respond with `HTTP/1.1 404 Not Found` (still including the CSP header).

**2. Custom TCP Audit Service (Port 8081):**
Listen on `127.0.0.1:8081` for raw TCP connections.
- When a client connects and sends the exact string `SCAN <TOKEN>\n` (where `<TOKEN>` is the extracted secret), the server should reply with `VALID\n` and close the connection.
- If the string does not match, reply with `REJECTED\n` and close the connection.

Ensure both services run concurrently when the application is executed. You can use threads for concurrent listening.
Leave the server running in the background when you are finished.