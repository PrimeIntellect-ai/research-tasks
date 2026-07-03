You are acting as a DevSecOps engineer. We are enforcing policy as code across our microservices and have identified a severe compliance failure in our legacy authentication service. It appears to be vulnerable to a JWT signature bypass (specifically, accepting `alg=none`).

Your task is to build an automated Python exploit/auditor to prove this vulnerability exists, which will be integrated into our continuous security pipeline.

Here are your instructions:
1. We have an architecture diagram located at `/app/diagram.png`. Using OCR (tesseract is installed), extract the text from this image. Somewhere in the text is an Issuer ID formatted as `ISSUER_ID: <value>`. You will need this `<value>` to craft your tokens.
2. Write a Python script at `/home/user/exploit_policy.py`.
3. The script must accept a single command-line argument: the target base URL (e.g., `http://localhost:8000`).
4. The script must craft a forged JWT token. The payload of the token must contain `{"admin": true, "iss": "<value_from_image>"}`. The header must be manipulated to bypass the signature check (using the `alg=none` vulnerability).
5. The script must use this token in the `Authorization: Bearer <token>` header to make a GET request to the target URL at the endpoint `/api/admin/dump`.
6. The script must print *only* the raw JSON string returned by the server to standard output and exit.

You can test your script by setting up a dummy Flask server if you wish, but the final evaluation will run your script against a hidden suite of 20 test servers. Ensure your script is robust and correctly implements the `alg=none` bypass without crashing.