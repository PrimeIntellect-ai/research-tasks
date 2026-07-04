You are a security engineer tasked with rotating credentials and hardening a local authentication service written in Rust. The service has been flagged for several security issues during a recent audit, and you need to patch them and provision new local TLS certificates.

Your objectives:

1. **TLS Certificate Management (Credential Rotation):**
   The local service requires a TLS certificate to serve HTTPS.
   Create a new directory `/home/user/certs`.
   Generate a new self-signed RSA 2048-bit certificate and unencrypted private key.
   Save the private key to `/home/user/certs/server.key` and the certificate to `/home/user/certs/server.crt`.
   The certificate must be valid for 365 days and have a Common Name (CN) of `localhost`.

2. **Fix Open Redirect Vulnerability:**
   The authentication service's source code is located at `/home/user/auth-server`. 
   Inspect `/home/user/auth-server/src/main.rs`. There is a `/login` endpoint that accepts a `next` query parameter to redirect the user after login. Currently, it is vulnerable to an open redirect attack (e.g., `?next=http://malicious.com`).
   Modify the Rust code so that if the `next` parameter starts with `http://` or `https://` (or `http:/`, `https:/` to catch simple bypasses), the server securely falls back to redirecting to `/dashboard`. 
   Relative paths (e.g., `/settings` or `/profile`) must continue to work normally.

3. **Content Security Policy Enforcement:**
   While editing the `/login` endpoint in the Rust source code, enforce a strict Content Security Policy.
   Add the HTTP header `Content-Security-Policy` with the value `default-src 'self';` to the response returned by the `/login` endpoint.

4. **Verify Your Changes:**
   Ensure the Rust project builds successfully by running `cargo check` or `cargo build` within `/home/user/auth-server`.
   Once you have completed the modifications and verified the build, create an empty file at `/home/user/task_complete` to signal that your work is done.

Do not change the port (8443) or the general server framework; only modify the route logic and headers as requested.