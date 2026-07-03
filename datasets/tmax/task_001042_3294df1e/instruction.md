You are acting as a security auditor tasked with setting up an auditing gateway for a restricted environment. 

A former administrator left behind a digital access badge containing a printed, base64-encoded secret token. This badge is located at `/app/admin_badge.png`. 

Your task is to:
1. Extract the base64-encoded token from the image using OCR (tesseract is available).
2. Decode the token to reveal the plaintext secret admin key.
3. Write and run a Python-based auditing TCP service listening on `localhost:9090`.
4. The service must handle raw TCP connections. When a client connects, it will send a base64-encoded payload followed by a newline (`\n`).
5. Your service must decode the incoming payload. If the decoded payload matches the plaintext secret admin key extracted from the badge, the service must immediately respond with the exact string `ACCESS_GRANTED\n` and close the connection. If it does not match, respond with `ACCESS_DENIED\n` and close the connection.
6. The service must run continuously to handle multiple sequential verification requests.

Make sure your Python service is running and listening on port 9090 before you consider the task complete.