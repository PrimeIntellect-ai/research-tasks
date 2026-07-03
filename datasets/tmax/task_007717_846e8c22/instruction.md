You are a security engineer tasked with rotating a compromised credential after a recent security incident. 

System logs indicate that an attacker bypassed our Content Security Policy (CSP), delivered a payload, and managed a sandbox escape that leaked an API token. 

Your task:
1. Parse the security log located at `/home/user/security.log`.
2. Find the log entry indicating a `[SANDBOX_ESCAPE]`. The line will explicitly state `Leaked token: <TOKEN>`.
3. Write a Rust program at `/home/user/rotate.rs` that reads the log file and extracts this compromised token.
4. The Rust program must output the exact extracted token to a file named `/home/user/leaked_key.txt`.
5. The Rust program must also craft a JSON payload to trigger the rotation service, written to `/home/user/rotation_payload.json`. The JSON must have exactly this structure and spacing (minify it, no extra spaces or newlines):
`{"action":"rotate","old_token":"<EXTRACTED_TOKEN>","new_token":"RUST_SECURE_TOKEN_2024"}`

You must write, compile (`rustc`), and run the Rust program to generate the required output files.