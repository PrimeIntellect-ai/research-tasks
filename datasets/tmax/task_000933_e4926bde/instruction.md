You are a forensics analyst responding to a compromised host. We have recovered a malicious binary at `/home/user/implant`. Our initial analysis indicates this executable acts as a local command-and-control service that accepts instructions via standard input.

The implant expects a token formatted similarly to a JWT: `Base64(Header).Base64(Payload).Signature`.
It uses standard Base64 (with padding).
We suspect the implant contains an authentication bypass vulnerability akin to the classic "JWT alg=none" flaw.

Your objective is to:
1. Reverse engineer or analyze the `/home/user/implant` ELF executable to determine the exact JSON keys and values expected in the Header and Payload to trigger the bypass and extract the hidden data.
2. Write a Rust program at `/home/user/recover.rs` (or within a Cargo project at `/home/user/recover`) that:
   - Generates the crafted token to bypass authentication (the signature portion can be any string, e.g., `dummy`).
   - Spawns the `/home/user/implant` binary as a child process.
   - Feeds the crafted token to the implant's standard input.
   - Captures the standard output of the implant and writes it exactly to `/home/user/flag.txt`.

Constraints & Requirements:
- Use Rust as the primary language for your exploit payload generation and execution.
- You may use any command-line tools (e.g., `strings`, `objdump`, `strace`) to analyze the binary.
- Ensure your Rust code correctly handles process I/O and standard Base64 encoding.

Once your Rust program executes successfully, the extracted secret must be saved in `/home/user/flag.txt`.