You are an incident responder investigating a security breach on a legacy authentication service. Attackers have been exploiting an open redirect vulnerability to steal authentication tokens, which are currently generated using a predictable and weak algorithm.

Your task consists of three parts:

**Part 1: Log Analysis & Firewall Configuration**
1. Analyze the web server logs located at `/home/user/logs/access.log` to identify the malicious IP address that has been exploiting the open redirect to send users to `http://evil.com/steal`.
2. Create a bash script at `/home/user/block.sh`. Inside this script, write the exact `iptables` command to append a rule to the `INPUT` chain that drops incoming TCP traffic on port `8080` originating from the malicious IP you identified.

**Part 2: Patching the Open Redirect**
The authentication logic is in a Rust project at `/home/user/auth_service`.
1. Open `/home/user/auth_service/src/auth.rs`.
2. Modify the `get_safe_redirect(requested_url: &str) -> String` function. It currently returns whatever URL is passed to it. Update it so that if the `requested_url` starts with exactly `https://trusted.corp/`, it returns the original URL. Otherwise, it must return the safe fallback: `https://trusted.corp/home`.

**Part 3: Securing Token Generation**
1. In the same `/home/user/auth_service/src/auth.rs` file, modify the `generate_secure_token(username: &str) -> String` function.
2. The current implementation just appends `_token` to the username. Replace this with a secure cryptographic hash. It must return the SHA-256 hex digest (lowercase) of the username concatenated immediately with the secret string `BIRD_IS_THE_WORD` (e.g., if username is "admin", hash the string "adminBIRD_IS_THE_WORD"). 
3. The `sha2` crate is already added to the project's `Cargo.toml`. 

Ensure that your Rust code compiles perfectly by running `cargo build` inside `/home/user/auth_service`. The automated verification will test your functions in `auth.rs` directly and verify your `block.sh` script.