You are a DevSecOps engineer tasked with auditing and fixing an internal authentication service before it is deployed to production. 

We have a vendored microservice located at `/app/vendored/jwt-auth-svc-1.2.0`. Because this system operates in a locked-down CI environment, you do not have internet access to download new packages. You must work with the existing vendored source.

Your task consists of several phases:

1. **Cryptographic Key Recovery:**
   The TLS private key for the service located at `/app/vendored/jwt-auth-svc-1.2.0/certs/server.key` is encrypted. The previous developer forgot the passphrase, but left a note saying it was exactly a 4-digit pin. You must crack the passphrase to use this key. Write the cracked 4-digit passphrase to `/home/user/key_password.txt`.

2. **Certificate Chain Assembly:**
   The service requires a full certificate chain to serve HTTPS properly. In `/app/vendored/jwt-auth-svc-1.2.0/certs/`, you will find `server.crt`, `intermediate.crt`, and `root.pem`. Assemble the correct full chain and save it to `/app/vendored/jwt-auth-svc-1.2.0/certs/fullchain.pem`. Ensure it validates correctly against the root.

3. **Package Configuration and Execution Fix:**
   The provided `Makefile` in the vendored package is broken. It has a deliberate typo in the `run` target (it tries to execute `pythn3` instead of `python3`) and fails to export a required environment variable `JWT_SECRET` (which you should set to `super-secret-dev-key`). Fix the `Makefile`.

4. **Security Vulnerability Remediation:**
   The service (specifically `/app/vendored/jwt-auth-svc-1.2.0/app/auth.py`) implements JWT validation. However, security scanners flagged that it is vulnerable to the "algorithm=none" bypass attack. Inspect the code and modify it so that it explicitly enforces the use of the `HS256` algorithm and rejects tokens with `alg=none`.

5. **Service Deployment:**
   Start the fixed service in the background using `make run`. 
   The service must simultaneously listen on:
   - `127.0.0.1:8080` (HTTP plaintext)
   - `127.0.0.1:8443` (HTTPS with your assembled `fullchain.pem` and decrypted key)
   
Leave the service running in the background. An automated verifier will connect to both ports to validate the certificate chain and test the authentication flow with both valid and malicious JWTs.