You are a DevSecOps engineer tasked with investigating a recent security incident and implementing policy-as-code to prevent future breaches. An attacker recently exploited a path traversal vulnerability in our internal Go-based ELF binary upload service to overwrite an SSH `authorized_keys` file and gain persistence. 

We have a screen recording of the attacker's terminal session captured by our internal monitoring tools, located at `/app/incident_logs.mp4`.

Your objectives are:

1. **Video Analysis & Token Generation:**
   The attacker's terminal scrollback in the video temporarily exposes the HMAC-SHA256 secret used by the application to sign JWTs. Extract this secret from the video (you may use `ffmpeg` to extract frames). Once you have the secret, generate a valid JWT token for the subject (`sub`) "admin" with an expiration (`exp`) set at least one hour in the future. Save this raw JWT string to `/home/user/admin_token.txt`.

2. **Policy-as-Code Scanner (Go):**
   We have captured a dataset of raw HTTP multipart/form-data upload requests in the directory `/app/uploads/`. Each file contains a raw HTTP POST request uploading an ELF binary. 
   Write a Go program at `/home/user/policy_scanner.go` that reads all `.req` files in `/app/uploads/` and evaluates them against our new security policies. A request is considered **VIOLATING (false)** if it fails ANY of the following checks, and **SAFE (true)** if it passes ALL of them:
   
   * **Path Traversal Check:** The `filename` parameter in the `Content-Disposition` header must not contain any path traversal sequences (e.g., `../`, `..\`, or absolute paths starting with `/`).
   * **ELF Architecture Check:** The uploaded file must be a valid 64-bit ELF executable (`EI_CLASS` = `ELFCLASS64`).
   * **SSH Key Hardening Check:** Our service expects developers to embed their public SSH keys within a custom ELF section named `.ssh_pubkey` for automated node provisioning. Your Go program must parse the ELF, locate the `.ssh_pubkey` section, and validate the contained SSH public key string. The key MUST be of type `ssh-ed25519`. If the key is missing, malformed, or uses a weak/legacy algorithm (like `ssh-rsa` or `ecdsa-sha2-nistp256`), the file is violating.

3. **Output Generation:**
   Your Go program must output its final verdicts to `/home/user/scan_results.json`. The format must be a JSON dictionary mapping the exact base filename of the request (e.g., `req_001.req`) to a boolean value indicating if it is safe (`true`) or violating (`false`).

Compile and run your Go program to generate the `/home/user/scan_results.json` file. Your scanner's accuracy will be evaluated programmatically against our hidden ground truth dataset. You must achieve an accuracy of at least 95%.