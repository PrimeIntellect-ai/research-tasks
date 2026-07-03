You are a DevSecOps engineer enforcing security policies as code. You need to perform three critical security tasks on the local system. Complete the following objectives:

**Objective 1: Token Generation (HMAC)**
A backend service requires an HMAC-SHA256 token to authorize administrative actions. 
1. Read the secret key located at `/home/user/keys/secret.key`.
2. Compute the HMAC-SHA256 signature of the exact string: `admin-access-request` using this secret key.
3. Save the resulting signature as a lowercase hex string into `/home/user/admin_token.txt`.

**Objective 2: SSH Hardening Policy**
You must configure secure, restricted SSH access for a new operations key.
1. Generate a new Ed25519 SSH key pair. Save the private key to `/home/user/.ssh/ops_key` (do not use a passphrase).
2. Authorize this key by adding the public key to `/home/user/.ssh/authorized_keys`.
3. To enforce network policy and minimize privileges, you must prepend the following exact restriction string to the public key entry in the `authorized_keys` file: `restrict,from="10.0.0.0/8" ` (ensure there is a space before the `ssh-ed25519` key type).

**Objective 3: HTTP Header Inspection**
A local staging web server is running on `http://127.0.0.1:8080`. You need to audit its HTTP response headers for missing security controls.
1. Fetch the HTTP headers from the root path (`/`) of `http://127.0.0.1:8080`.
2. Check for the presence of the following two security headers:
   - `X-Frame-Options`
   - `Strict-Transport-Security`
3. Create an audit log at `/home/user/header_audit.log`. For each of the above headers that is missing from the response, append a line in the exact format: `MISSING: <Header-Name>`. (For example: `MISSING: X-Frame-Options`). If a header is present, do not write anything for it.

Ensure all output files (`admin_token.txt`, `authorized_keys`, `header_audit.log`) are correctly formatted and located in the specified paths.