You are a security auditor tasked with securing a Python web application that uses a custom-vendored authentication library. The system has multiple vulnerabilities, including an open redirect, insecure token validation, and improper access controls.

Environment Overview:
- The main web application code is located in `/app/server/app.py`.
- The application uses a vendored version of the `PyJWT` package (version 2.4.0) located at `/app/pyjwt-2.4.0/`.
- Logs are stored in `/app/logs/access.log`.
- An automated security testing tool is available at `/app/tester/run_tests.py`.

Your objectives:
1. **Audit and Fix the Vendored Package:** The vendored `PyJWT` library at `/app/pyjwt-2.4.0/` has been deliberately perturbed with a bad patch. It currently suffers from an algorithm confusion / "none" algorithm vulnerability. When verifying a token, if the token specifies `"alg": "none"`, the signature verification is bypassed entirely, even if a secret key was passed to the `decode` function. Audit the source (specifically `jwt/api_jws.py` or `jwt/api_jwt.py`) and fix this logic so that tokens with the "none" algorithm are strictly rejected when a verification key is provided.
2. **Fix the Open Redirect Vulnerability:** The login endpoint in `/app/server/app.py` reads a `next` query parameter and blindly redirects the user to that URL after successful authentication. Modify `app.py` to validate the `next` parameter. It should only permit relative redirects (the path must start with a single `/`, and must not start with `//` or an absolute URI scheme). If the `next` parameter is invalid or missing, it should default to `/dashboard`.
3. **Secure File Permissions:** The directory `/app/logs/` and the log file `/app/logs/access.log` currently have overly permissive access rights (world-readable/writable). Change the permissions of the `/app/logs/` directory to `700` and `/app/logs/access.log` to `600`.
4. **Log Analysis and Token Auditing:** Write a Python script at `/home/user/analyze_logs.py` that parses the `/app/logs/access.log` file. 
    - Extract all JWT tokens present in the `Authorization: Bearer <token>` headers or `token=` URL parameters logged in the file.
    - Using your patched `/app/pyjwt-2.4.0/` library, attempt to validate each extracted token. The server's secret key is `"supersecret_key_123"`.
    - Your script must count the total number of mathematically valid, unexpired tokens found in the log file, and write this integer strictly as a plain text number to `/home/user/valid_tokens_count.txt`.

You can iteratively test the web application's security posture by running `python3 /app/tester/run_tests.py --score-only`. This script outputs a numeric security score between 0 and 100. You must achieve a score of 100.