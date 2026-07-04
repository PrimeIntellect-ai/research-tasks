You are acting as a network security engineer. We need to deploy a secure, minimal file upload handler using a Bash script, but it must be protected against path traversal attacks and secured via TLS.

Here are your instructions:

1. **Extract Authentication Token**: We have a network diagram image located at `/app/network_topology.png`. Use OCR (e.g., `tesseract`) to extract the text from this image. Somewhere in the text is an authentication token in the format `Token: <string>`. Extract this `<string>`.

2. **Generate TLS Certificates**: Generate a self-signed SSL certificate (`server.crt`) and private key (`server.key`) valid for `localhost`. Place them in `/home/user/certs/`. 

3. **Create the Upload Server**:
   Write a Bash script at `/home/user/upload_server.sh` that uses `socat` or `ncat` to listen on TCP port `8443` with TLS enabled, using the certificate and key you generated.
   The server must process incoming HTTPS POST requests.
   
   Security Requirements:
   - **Authentication**: The server must read the HTTP headers and verify that the `X-Auth-Token` header exactly matches the token extracted from the image. If missing or incorrect, respond with `HTTP/1.1 401 Unauthorized\r\n\r\n`.
   - **Path Traversal Protection**: The server expects the requested path to be in the format `POST /upload?file=<filename>`. Inspect the `<filename>`. If the filename contains the string `../` or starts with `/`, it must be rejected with `HTTP/1.1 403 Forbidden\r\n\r\n`.
   - **Success**: If the token is valid and the filename is safe, respond with `HTTP/1.1 200 OK\r\n\r\nSuccess`.

4. **Run the Server**:
   Execute your Bash script in the background so it is actively listening on `127.0.0.1:8443`.

Ensure your script handles the HTTP request parsing correctly in Bash and keeps running to accept multiple requests (e.g., using a loop or a tool like `socat` with `fork` or `ncat -k -l`).

Do not use Python, Ruby, or other languages for the server; it must be implemented as a Bash script leveraging command-line networking tools.