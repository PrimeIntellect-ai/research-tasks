You are a red-team operator preparing an evasion payload for an upcoming engagement. 

During previous reconnaissance, your team extracted a stripped binary from the target's network, located at `/app/auth_encoder`. This tool is used by the target's administrators to encode authorized commands before sending them through a heavily monitored network boundary. 

We need to generate our own payloads without relying on the target's clunky binary. There are a few hurdles:
1. **Authentication Flow Testing & Cracking:** The `/app/auth_encoder` binary is protected. It requires two arguments: a 4-digit PIN and the input string to encode (e.g., `/app/auth_encoder 0000 "my_payload"`). If the PIN is incorrect, it exits with status code 1. You must brute-force this 4-digit PIN to unlock the encoding functionality.
2. **Payload Encoding/Decoding Analysis:** Once you have the PIN, observe how the binary transforms input strings. You need to reverse-engineer or black-box analyze its encoding scheme. 
3. **Reimplementation in Rust:** The binary is too slow and conspicuous to run on our C2 server. You must write a drop-in replacement in Rust. Create a new Rust project at `/home/user/evasion_payload`. Your Rust application must compile to an executable that takes a *single* argument (the raw string) and prints the exact encoded output that the original binary would produce with the correct PIN. 

**Requirements:**
- Your Rust project must be located exactly at `/home/user/evasion_payload`.
- Build a release version of your binary so it resides at `/home/user/evasion_payload/target/release/evasion_payload`.
- The executable must output *only* the encoded payload to `stdout` (no trailing newlines unless the original binary produces one, exact byte-for-byte match).
- You can use standard tools (e.g., `strings`, `objdump`, `bash`, `python`) to crack the PIN and analyze the binary.
- Use `cargo` to manage and build your Rust project. You may use common crates like `base64` if you deem them necessary by specifying them in your `Cargo.toml`.

Your final deliverable is the compiled release binary at `/home/user/evasion_payload/target/release/evasion_payload`. Automated verification will extensively fuzz your binary against the original using random strings to ensure bit-exact equivalence.