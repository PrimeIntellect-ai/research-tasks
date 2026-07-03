You are a DevSecOps engineer investigating a recent security incident and deploying a new policy-as-code enforcement service to prevent future unauthorized execution.

Part 1: Incident Analysis (Video & Reverse Engineering)
We captured a recording of the attacker's terminal session in `/app/incident_record.mp4`. Extract the frames and analyze the video. Around the 3-second mark, the attacker accidentally types the secret 16-character encryption key they used for their payloads before clearing the screen. Find this key.
Additionally, you will find a compiled ELF binary at `/app/legacy_decoder.bin`. Reverse engineer this binary to determine the encryption algorithm used (it is a standard encoding layered with a simple bitwise operation using the key).

Part 2: Policy Enforcement Service
Create an HTTP service in Python (or Bash using netcat) that listens on `127.0.0.1:9000`. This service must act as a secure execution sandbox and enforce our new policy.
- Endpoint: POST `/execute`
- The request body will be JSON containing:
  `{"payload": "<base64_string>", "checksum": "<sha256_hex>"}`
- Your service must:
  1. Decode the base64 payload.
  2. Decrypt the decoded bytes using the algorithm discovered in Part 1 and the 16-character key extracted from the video.
  3. Verify that the SHA256 hash of the decrypted plaintext exactly matches the provided `checksum`. If it does not, return HTTP 403 Forbidden.
  4. If the checksum matches, execute the decrypted plaintext as a bash command in a sandboxed manner (e.g., standard subprocess execution with a 2-second timeout, running inside the `/tmp/sandbox` directory which you must create).
  5. Return HTTP 200 OK with the stdout of the executed command as the response body.

Ensure your service is robust and remains running in the background to handle multiple requests from our automated verifier. Create the `/tmp/sandbox` directory before starting the service.