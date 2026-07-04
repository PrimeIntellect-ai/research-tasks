You are a compliance analyst generating an audit trail for an internal authentication service written in Rust. We suspect the service is vulnerable to a classic JWT "alg: none" bypass, and we need you to prove it by generating a forged token and capturing the successful authentication logs.

You have been provided with a compiled Rust binary at `/home/user/auth_verifier` (and its source code in `/home/user/auth_service/src/main.rs` for inspection). 

Your task:
1. Review the Rust source code to understand how the application parses JWTs and what claims it expects to grant admin access.
2. Verify the integrity of the compiled binary by calculating its SHA-256 hash and saving the hash string (just the hex hash, nothing else) to `/home/user/binary_hash.txt`.
3. Create a forged JWT that exploits the `alg: none` vulnerability. The token must include the claims required to be recognized as an administrator by the service, and the subject (`sub`) must be set to `auditor`.
4. Save your forged JWT exactly as a single string to `/home/user/forged_token.jwt`.
5. Run the `/home/user/auth_verifier` binary, passing the path to your forged token as the first argument. Capture its standard output and save it to `/home/user/audit_trail.log`.

Constraints:
- You may write a script in Rust or Bash to generate the token, or you can construct it manually.
- The base64url encoding must not contain padding.
- The output in `audit_trail.log` must show a successful authentication message for the administrator role.