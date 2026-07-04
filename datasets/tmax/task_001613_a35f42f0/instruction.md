You are a site administrator responsible for managing an automated user provisioning pipeline. The pipeline processes JSON configuration files submitted by department heads to create user accounts, set up network synchronization settings, apply ACLs, and enforce disk quotas.

Recently, malicious or malformed requests have been breaking the pipeline. You need to write a strict validator in Rust to sanitize these incoming JSON profiles.

Additionally, your project must integrate a heavily used internal package, `acl-manager-rs`, to perform dry-run ACL checks.

Here are your instructions:

1. **Fix the Vendored Package:**
   There is a pre-vendored third-party package located at `/app/acl-manager-rs`. It is currently failing to compile due to a deliberate perturbation in its build system (a missing environment variable handling in `build.rs` or a syntax error in the source code). Identify the issue, fix the package, and ensure it can compile using `cargo build`.

2. **Create the Provisioner Validator:**
   Initialize a new Rust binary project at `/home/user/provisioner`.
   Add `/app/acl-manager-rs` as a local dependency in your `Cargo.toml`.
   
   Your program must accept a JSON file path via the command line:
   `/home/user/provisioner/target/release/provisioner <path_to_json>`
   
   The JSON profiles have the following schema:
   ```json
   {
     "username": "string",
     "quota_mb": "number",
     "ssh_key": "string",
     "sync_ip": "string"
   }
   ```

3. **Validation Rules (The Core Task):**
   Your program must read the JSON file and strictly validate it. If the profile is completely valid, the program MUST exit with code `0`. If ANY validation rule fails, it MUST exit with a non-zero exit code (e.g., `1`).
   
   Rules:
   * `username`: Must be between 1 and 32 characters long. Allowed characters are lowercase letters, numbers, and underscores only. No path traversal components (like `.` or `/`).
   * `quota_mb`: Must be an integer between 1 and 10240 (inclusive).
   * `ssh_key`: Must strictly start with either `ssh-rsa ` or `ssh-ed25519 `. It must not contain any shell metacharacters (e.g., `;`, `|`, `&`, `$`, `>`, `<`).
   * `sync_ip`: Must be a strictly valid, well-formed IPv4 address (e.g., `192.168.1.50`).

4. **Testing against the Corpora:**
   We have provided two test corpora:
   * `/app/corpora/clean/` contains valid JSON profiles.
   * `/app/corpora/evil/` contains malformed or malicious profiles (e.g., negative quotas, SQL/Bash injections in keys, invalid IPs, path traversals).
   
   Ensure your binary strictly passes the clean corpus and firmly rejects everything in the evil corpus. Build your final binary in release mode.