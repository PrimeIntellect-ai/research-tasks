You are a security engineer responsible for rotating credentials and securing a legacy internal service. 

We have a vendored, lightweight web server located at `/app/legacy-tls-server-1.0`. It has been flagged by our security team for two reasons:
1. Its TLS certificates are expired and need rotation.
2. It has a known Local File Inclusion (LFI) vulnerability. Until the developers rewrite it, you must deploy it inside a strict sandbox to limit the blast radius.

Your objectives:

1. **Fix the Package**: The vendored package at `/app/legacy-tls-server-1.0` has a broken `Makefile`. Fix the perturbation in the `Makefile` so the application can be started. (Hint: look at the `start` target).

2. **Rotate Credentials**:
   - Generate a new self-signed X.509 certificate and an RSA 4096-bit private key.
   - The private key MUST be encrypted with AES-256-CBC.
   - Store a strong, randomly generated passphrase in `/home/user/passphrase.key` (with restrictive `0400` permissions).
   - Place the certificate at `/home/user/certs/server.crt` and the encrypted key at `/home/user/certs/server.key`.

3. **Process Isolation (Sandboxing)**:
   - Write a bash script at `/home/user/secure_runner.sh` that starts the web server on port `8443`.
   - The script must use `bwrap` (Bubblewrap) to sandbox the Python application.
   - The sandbox must be read-only where possible, bind-mount only the required certificates, application directories, and standard system libraries required for Python to run.
   - **Crucially:** Ensure that the directory `/home/user/secrets` (and the `flag.txt` inside it) is absolutely inaccessible from within the sandbox.
   - The server process needs the passphrase to decrypt the key at startup. Pass it securely (e.g., via a temporary file descriptor or an environment variable that is carefully managed in the script) to the application as required by its start command: `python3 server.py --cert <cert> --key <key> --pass <pass>`.

When you are done, execute your `/home/user/secure_runner.sh` in the background so the server is listening on `127.0.0.1:8443`. Then, output a file `/home/user/deployment_done.log` containing the text "READY". 

An automated test will measure the security of your sandbox by calculating the sandbox isolation metric (the percentage of LFI attacks that are successfully blocked).