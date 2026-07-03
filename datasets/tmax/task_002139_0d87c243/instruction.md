As a compliance analyst, you are responsible for generating verifiable audit trails for security incidents. We have recovered a suspicious binary involved in a recent incident, located at `/home/user/evidence.elf`. 

Your task is to create a Rust-based utility that analyzes this binary, generates a proof-of-concept (PoC) payload to demonstrate a theoretical control-flow hijack, and produces a cryptographic audit log.

Specifically, you must write a Rust program (initialize it in `/home/user/audit_tool`) that accomplishes the following:
1. **ELF Analysis:** Programmatically determine the virtual memory address of the `.text` section of `/home/user/evidence.elf`. (You may use standard Linux utilities like `readelf` invoked via Rust's `std::process::Command`, or parse it directly).
2. **Payload Delivery/Crafting:** Construct a malicious payload file and save it to `/home/user/payload.bin`. The payload must consist exactly of:
   - 72 bytes of NOP instructions (`0x90`).
   - Followed immediately by the 64-bit (8 bytes) Little-Endian representation of the `.text` section's virtual address discovered in step 1.
3. **Cryptographic Hashing:** Compute the SHA-256 hash of the generated `payload.bin` file.
4. **Audit Trail Generation:** Output a JSON formatted audit log to `/home/user/audit_log.json` containing exactly these two keys:
   - `"text_address"`: A string representation of the `.text` section's virtual address in lowercase hexadecimal format, prefixed with "0x" (e.g., `"0x401000"`).
   - `"payload_sha256"`: A string of the SHA-256 hash of the payload in lowercase hexadecimal.

Your Rust project should be runnable via `cargo run` inside `/home/user/audit_tool`. You must successfully run your tool so that `/home/user/payload.bin` and `/home/user/audit_log.json` are generated and available on disk.