You are a mobile build engineer maintaining a custom CI/CD deployment gate. Part of the pipeline involves verifying a stamped release image, calculating a checksum of the build artifact, and starting a lightweight C-based HTTP server to authorize the final deployment.

You must accomplish the following tasks:

1. **Extract Release Metadata**
   A release tag image is located at `/app/release_tag.png`. It contains the target semantic version and a secret authorization token. Use OCR (tesseract is available) to extract this text. The expected format in the image is:
   ```
   VERSION: <semver>
   TOKEN: <auth_token>
   ```

2. **Calculate Checksum (C implementation)**
   There is a mock build artifact located at `/app/payload.bin`. Write a C function that calculates the 8-bit XOR checksum of the entire file (start with a checksum value of 0, and XOR each byte of the file sequentially). 

3. **Develop the Deployment Gate (C implementation)**
   Write and compile a C program (`/home/user/deploy_gate.c` -> `/home/user/deploy_gate`) that implements a simple HTTP deployment gate server.
   - The server must bind to `127.0.0.1` on port `8080`.
   - It must listen for incoming HTTP `GET` requests to the path `/deploy`.
   - It must validate the `Authorization` header. The request must include: `Authorization: Bearer <auth_token>` (using the exact token extracted from the image).
   - If the token is missing or invalid, return an `HTTP/1.1 401 Unauthorized` response.
   - If the token is valid, it must return an `HTTP/1.1 200 OK` response with the `Content-Type: application/json` header and the following JSON body:
     ```json
     {"status": "ready", "version": "<semver>", "checksum": <integer_checksum>}
     ```
     *(Where `<semver>` is the exact version string extracted from the image, and `<integer_checksum>` is the decimal integer representation of the 8-bit XOR checksum of `/app/payload.bin`)*.

4. **Execution**
   Compile your C program and start it in the background so that it is actively listening on port 8080. Ensure it does not terminate immediately after serving one request (use a standard accept loop). 

Automated verifiers will connect to `127.0.0.1:8080` to validate your deployment gate.