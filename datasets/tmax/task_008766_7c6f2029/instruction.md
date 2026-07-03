You are a penetration tester investigating a compromised web server. The attackers managed to steal an admin session, and you need to figure out the original authentication token to understand the scope of the breach.

During your investigation, you discovered that the server's authentication daemon is vulnerable: it occasionally spawns worker processes and passes the raw plaintext authentication tokens as command-line arguments, which were leaked and captured via `/proc/self/cmdline` monitoring.

You have the following artifacts in your workspace (`/home/user/`):
1. `/home/user/auth.log`: The web server's security log containing session hashes.
2. `/home/user/cmdlines.txt`: A log of captured process command lines.
3. `/home/user/auth_daemon`: The compiled authentication binary used by the server.

Your objective is to recover the plaintext admin token by correlating the logs and reverse-engineering the hashing logic. 

Perform the following steps:
1. **Analyze the Logs**: Parse `/home/user/auth.log` to find the SHA-256 hash associated with the successful login of the user `admin`.
2. **Reverse Engineer the Binary**: Analyze the compiled binary `/home/user/auth_daemon` using standard Linux CLI tools to find a hardcoded cryptographic salt. The salt is a string that starts with the prefix `SALT_`.
3. **Parse Leaked Tokens**: Extract the plaintext tokens from `/home/user/cmdlines.txt`. They are passed to the worker processes via the `--token` argument.
4. **Develop a Rust Tool**: 
   - Create a new Rust binary project at `/home/user/token_recovery` (use `cargo new`).
   - Add necessary dependencies (like `sha2`) to your `Cargo.toml`.
   - Write a Rust program that computes the SHA-256 hash of each extracted token concatenated with the salt (format: `<token><salt>`).
   - Compare the resulting hashes against the `admin` hash found in `auth.log`.
5. **Output**: Once your Rust program finds the matching token, it must write the exact plaintext token (without the salt or any extra characters/newlines) to `/home/user/recovered_admin_token.txt`.

Ensure your Rust tool is fully automated. You may use shell commands to inspect the files before writing your Rust code.