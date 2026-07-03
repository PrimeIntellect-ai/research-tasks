You are a DevSecOps engineer enforcing policy as code. We need a lightweight, standalone Policy Decision Point (PDP) webhook that validates incoming execution requests for an internal sandboxing system.

To secure this webhook, the authorization token is provided as an image artifact (to prevent automated scraping from configuration files). The image is located at `/app/policy_token.png`.

Your task is to write and run a Python HTTP server that acts as this webhook. 

Requirements for the server:
1. Listen on exactly `127.0.0.1:8000`.
2. Expose a single endpoint: `POST /validate`.
3. Read the authorization token from `/app/policy_token.png` using OCR (e.g., using `pytesseract`). The token will be alphanumeric. Be sure to strip any trailing whitespace or newlines.
4. When a request is received on `POST /validate`:
   - First, check the `X-Policy-Token` HTTP header. If it is missing or does not perfectly match the OCR-extracted token, return an HTTP `401 Unauthorized` status.
   - If the token is valid, parse the JSON request body. The payload will have the format: `{"command": "<base64_encoded_string>"}`.
   - Base64-decode the `command` string to get the raw command.
   - Run a pattern-matching check on the decoded command to detect a specific exploit payload signature. The signature is a regex pattern designed to catch common x86 relative jump/call shellcode sequences: `(?:0x)?[eE]9\s?[0-9a-fA-F]{8}`.
   - If the decoded command matches this regex pattern, reject the request by returning an HTTP `403 Forbidden` status.
   - If the token is valid and no exploit pattern is detected, allow the request by returning an HTTP `200 OK` status.

Write the Python script, install any necessary dependencies (like `Flask` or `pytesseract`, and system packages like `tesseract-ocr` if needed), and start the server so it is actively listening on port 8000. Leave the server running in the background.