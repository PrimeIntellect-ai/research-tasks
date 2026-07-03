You are acting as a security engineer tasked with rotating credentials and securing a legacy authentication service. 

We have a simple authentication server written in C located at `/home/user/auth_server.c`. This server handles two endpoints:
1. `/login` - Accepts a username and password. If successful, it sets an authentication token in the `AuthToken` cookie and redirects the user to a URL provided in the `next` query parameter.
2. `/rotate` - Accepts a new password, provided the user has a valid `AuthToken` cookie. If it fails, it echoes the username provided in the request back to the user.

Currently, this server suffers from multiple vulnerabilities:
- **Predictable Token Generation:** The `AuthToken` is generated insecurely and can be guessed/forged.
- **Open Redirect:** The `/login` endpoint blindly redirects the user to the `next` parameter without validation.
- **Cross-Site Scripting (XSS):** The `/rotate` endpoint echoes unescaped user input (username) into the HTTP response body.

Your task is to:
1. **Develop an Exploit Script:** Write a Python script at `/home/user/test_vulns.py` that starts the C server (compiled to `/home/user/auth_server_vulnerable` on port 8080) and exploits these vulnerabilities. 
    - It must forge a valid token for the user `admin`.
    - It must trigger the open redirect by passing `http://malicious.example.com` to the `next` parameter, verifying the `Location` header.
    - It must send an XSS payload `<script>alert(1)</script>` as the username to `/rotate` and verify the payload is reflected in the response body.
    - The script should write the string `VULNERABLE: OPEN_REDIRECT, XSS, FORGED_TOKEN` to `/home/user/exploit_results.txt` if all exploits succeed.

2. **Patch the C Server:** Modify `/home/user/auth_server.c` to fix these vulnerabilities.
    - **Open Redirect:** Only allow redirects to relative paths (must start with `/` and not `//`). If an invalid redirect is provided, default to `/dashboard`.
    - **Token Generation:** Modify the token generation function to read 16 bytes from `/dev/urandom` and hex-encode them instead of the current weak mechanism.
    - **XSS:** Ensure the username echoed in the `/rotate` response is safely HTML-entity encoded (at least replace `<` with `&lt;` and `>` with `&gt;`).

3. **Verify the Fix:** Compile your patched code to `/home/user/auth_server_fixed`. Run your `/home/user/test_vulns.py` script against this fixed server (running on port 8081). The script should detect that the exploits now fail and output the string `SECURE: EXPLOITS_FAILED` to `/home/user/fixed_results.txt`.

You must manage the compilation, backgrounding of the server processes, and execution of the Python script. Ensure all servers are gracefully terminated after your scripts complete.