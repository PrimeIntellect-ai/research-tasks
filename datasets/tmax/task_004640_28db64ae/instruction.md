You are a penetration tester tasked with analyzing a leaked video of an administrator's session and remediating the vulnerabilities found in their custom tools.

A video of the administrator's terminal session has been recovered and is located at `/app/admin_session.mp4`. In this video, the administrator runs a custom Rust-based vulnerability scanner to log into a remote server. Unfortunately, the scanner is poorly written and leaks sensitive credentials (SSH passphrases) via command-line arguments visible in `/proc`, which you will be able to observe in the video.

Your objectives are:
1. **Analyze the Video**: Use `ffmpeg` and any available CLI tools (like `tesseract` for OCR, which is pre-installed) to extract frames from `/app/admin_session.mp4` and identify the exact leaked SSH passphrase used by the administrator. Write this passphrase to `/home/user/leaked_passphrase.txt`.
2. **Audit and Fix the Rust Code**: The source code for the custom scanner is located at `/home/user/rusty_scanner/`. It currently takes the passphrase via CLI and spawns a child `ssh` process passing the passphrase directly in the command line, causing a CWE-214 (Information Exposure). Refactor `src/main.rs` to securely pass the passphrase to the child process (e.g., via `stdin` or a secure temporary file) so it is no longer visible in `/proc`.
3. **SSH Hardening and File Permissions**: Ensure the scanner enforces strict access controls. Modify the Rust code to check that the provided SSH key file has permissions of exactly `0600` before attempting to use it. If the permissions are broader, the program should abort. Additionally, generate a hardened SSH config file at `/home/user/.ssh/config` that disables root login and enforces key-based authentication.

The automated verifier will compile your modified Rust project. It will run the scanner under test conditions while aggressively polling `/proc` to catch any leaked arguments. 

**Verification Metric**:
The automated test will calculate a `leak_rate` (number of times the passphrase was detected in `/proc` divided by the total number of test executions). Your patched code must achieve a `leak_rate <= 0.0` (zero leaks). The verifier will also check that your program correctly rejects files with improper permissions.