You are a DevSecOps engineer tasked with enforcing policy-as-code and fixing a critical vulnerability in an internal application. 

We have an internal web application located at `/home/user/server.py` that uses a custom-vendored JWT library to authenticate requests to its `/data` endpoint. We suspect that the vendored JWT library contains a dangerous backdoor or logic flaw related to algorithm validation, specifically allowing the "none" algorithm to bypass signature checks.

Your objectives are:

1. **Vulnerability Analysis & Patching:**
   Analyze the vendored package located at `/app/vendored/pyjwt_custom-1.0.0/`. Find the vulnerability that accepts `alg="none"` (or `None`) and bypasses signature verification. Modify the library's source code to reject tokens with a `none` algorithm (it should raise an Exception or return an error as it does for invalid signatures).

2. **Package Installation:**
   Install the patched `pyjwt_custom` library into your local Python environment (e.g., using `pip install -e /app/vendored/pyjwt_custom-1.0.0/`). You do not have internet access, so you must rely entirely on the vendored source.

3. **File Permission & Access Control (Policy Enforcement):**
   The application reads its JWT signing secret from `/home/user/keys/secret.key`. As part of our strict policy-as-code enforcement, the application checks the file permissions of this key file. It will refuse to start if the file is accessible to anyone other than the owner. You must fix the file permissions of `/home/user/keys/secret.key` to strictly read-only for the owner (`0400`).

4. **Service Bring-up:**
   Once the package is patched and installed, and the key permissions are secured, start the API server by running `python3 /home/user/server.py`. The server will listen on `127.0.0.1:8000`. Leave the server running in the background or foreground so that our automated security scanner can test it.

Our automated verifier will send HTTP requests to your server to verify that:
- The server starts successfully (meaning permissions are correct).
- Valid signed tokens are accepted.
- Tokens using `alg: "none"` are strictly rejected with an HTTP 401 Unauthorized status.