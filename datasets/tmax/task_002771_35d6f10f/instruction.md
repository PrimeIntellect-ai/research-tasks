You are an internal network security engineer. While inspecting traffic on your company's network, you identified suspicious activity targeting an internal Bash-based administrative web service. 

The source code for this service is vendored in the container at `/app/bash-admin-server/`. The server runs via `socat` and executes Bash scripts as CGI endpoints.

Currently, the server is offline due to a broken deployment script, and the codebase contains severe vulnerabilities. Your objective is to fix the server, patch the vulnerabilities, extract a hidden validation token from an ELF binary, and bring the server back online securely.

Perform the following tasks:

1. **Fix the Vendored Package:**
   The start script `/app/bash-admin-server/start.sh` contains a typo and an incorrect path configuration that prevents it from starting. Fix the script so that it properly uses `socat` to listen on `127.0.0.1:8080` and serves the `cgi-bin` directory correctly.

2. **Patch Vulnerabilities:**
   - **Open Redirect:** Inspect `/app/bash-admin-server/cgi-bin/login.sh`. It blindly redirects users based on the `next` query parameter. Patch it using Bash so that it only allows relative redirects (the `next` parameter MUST start with `/` and MUST NOT start with `//`). If the payload is invalid, redirect to `/index.sh`.
   - **Command Injection:** Inspect `/app/bash-admin-server/cgi-bin/diag.sh`. It takes an `ip` query parameter and pings it, but is vulnerable to command injection. Patch it using pure Bash to strictly validate that the `ip` parameter is a valid IPv4 address (e.g., `1.1.1.1`) before executing the `ping` command. If invalid, output a `400 Bad Request` HTTP status.

3. **ELF Analysis & SSH Key Management:**
   The server has an endpoint `/app/bash-admin-server/cgi-bin/add_key.sh` which delegates SSH key validation to a compiled ELF binary located at `/app/bash-admin-server/bin/key_validator`.
   - Analyze the `key_validator` ELF binary. It rejects any SSH public key that does not contain a specific secret corporate identifier in its comment field.
   - Write a Bash script at `/home/user/generate_key.sh` that, when executed, generates a new, password-less ED25519 SSH keypair at `/home/user/admin_key` and `/home/user/admin_key.pub`. The public key MUST contain the exact secret corporate identifier discovered from the ELF binary as its comment.

4. **Bring the Service Online:**
   Once all fixes are in place, run your patched `/app/bash-admin-server/start.sh` as a background process so the service is listening on `127.0.0.1:8080`. 

Leave the server running. Automated tests will send HTTP requests to `127.0.0.1:8080` to verify your patches and will execute your `/home/user/generate_key.sh` script to verify SSH key generation.