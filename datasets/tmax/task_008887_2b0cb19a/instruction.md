You are an incident responder investigating a compromised server. Attackers recently exploited a vulnerability in a Rust-based web application to conduct a phishing campaign via an open redirect, and managed to access the deployment pipeline.

Your task is to remediate the vulnerability, harden the deployment SSH access, and prepare a sandboxed execution script.

1. **Fix the Open Redirect:**
The source code for the Rust web server is located at `/home/user/app`.
The application uses `axum` and has a `/login` endpoint in `/home/user/app/src/main.rs`. 
Currently, it blindly redirects users to whatever URL is provided in the `next` query parameter.
Modify the code to validate the `next` parameter:
- It must be a relative path.
- It must start with exactly one `/` character (e.g., `/profile`).
- It must **not** start with `//` (to prevent protocol-relative URL redirects like `//evil.com`).
- If the `next` parameter is missing, empty, or fails the above validation, redirect to the default `/dashboard`.
After fixing the code, compile the application using `cargo build --release` inside `/home/user/app`.

2. **Harden Deployment SSH Access:**
The attackers compromised the previous deployment key. You need to create a new, restricted SSH key for automated deployments.
- Generate a new Ed25519 SSH key pair at `/home/user/.ssh/deploy_key` with no passphrase.
- Add the newly generated public key to `/home/user/.ssh/authorized_keys`.
- Prepend the public key entry in `authorized_keys` with the following SSH restrictions to prevent unauthorized use if the key is leaked again:
  `no-pty,no-port-forwarding,no-X11-forwarding,command="/home/user/run_sandboxed.sh"`

3. **Sandboxed Execution Script:**
Write a bash script at `/home/user/run_sandboxed.sh` that will be triggered by the deployment key.
The script must:
- Include a `#!/bin/bash` shebang.
- Execute the compiled web application `/home/user/app/target/release/web_app` using `bwrap` (Bubblewrap) for process isolation.
- Use the following exact `bwrap` arguments to sandbox the app:
  `bwrap --ro-bind / / --dev /dev --unshare-all --share-net --bind /home/user/app /home/user/app /home/user/app/target/release/web_app`
- Make the script executable (`chmod +x /home/user/run_sandboxed.sh`).

Complete all three steps to secure the system.