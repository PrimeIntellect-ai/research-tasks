You are a security auditor investigating an undocumented service on a Linux machine. You have discovered a binary at `/home/user/app_binary` and a corresponding TLS certificate at `/home/user/cert.pem`.

Your task is to write a Rust-based auditing tool to extract security metadata and generate a network firewall policy based on your findings.

Step 1: Write a Rust program
Create a Cargo project in `/home/user/elf_auditor`. Your Rust program must:
1. Parse the ELF file `/home/user/app_binary`.
2. Extract the Entry Point memory address of the ELF (formatted as a lowercase hex string with the `0x` prefix).
3. Extract the raw string contents of the custom ELF section named `.audit_policy`. This section contains a configuration string specifying a port (e.g., `PORT=XXXX`).
4. Parse the TLS certificate at `/home/user/cert.pem` and extract its Subject Common Name (CN).
5. Output these three pieces of extracted information into a JSON file at `/home/user/audit_report.json` with the exact keys: `entry_point`, `policy`, and `cert_cn`.

Step 2: Generate Firewall Rules
Based on the port specified in the `.audit_policy` section of the binary, create a bash script at `/home/user/fw_config.sh`. This script should contain exactly two `iptables` commands to enforce the following policy:
1. Allow inbound TCP traffic to that specific port ONLY from the IP address `192.168.1.100`.
2. Drop all other inbound TCP traffic to that specific port.

Requirements:
- Ensure the Rust program compiles successfully with `cargo build`.
- You may use external crates (like `elf`, `x509-parser`, `openssl`, etc.) by adding them to your `Cargo.toml`.
- The `fw_config.sh` script should be plain text with one command per line and no extra scripting wrapper.

Run your Rust program to generate `/home/user/audit_report.json`, and manually create `/home/user/fw_config.sh` with the correct rules based on the program's output.