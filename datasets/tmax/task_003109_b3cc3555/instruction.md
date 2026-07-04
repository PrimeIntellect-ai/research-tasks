You are a network engineer analyzing a suspected command-and-control (C2) intrusion that utilizes VoIP traffic for data exfiltration and signaling. You have been provided with intercepted data and need to complete a multi-stage analysis and remediation workflow.

**Stage 1: Audio Analysis and Network Policy**
You intercepted a suspicious audio payload at `/app/intercepted.wav`. This file contains an automated spoken message detailing the backup C2 server's IP address and port.
1. Transcribe the audio file to extract the hidden IP address and port. 
2. Based on the transcription, write a bash script at `/home/user/firewall_block.sh` containing the exact `iptables` command to drop all outbound TCP traffic to that specific IP and port. 

**Stage 2: Reverse Engineering and Data Processing**
The attackers use a custom binary to obfuscate data before transmitting it over the network. We have recovered a stripped ELF binary at `/app/c2_obfuscator` which performs this transformation. 
1. Reverse engineer the `/app/c2_obfuscator` binary. You may use tools like `objdump`, `strace`, `gdb`, or sandbox execution to analyze its behavior. It reads raw bytes from `stdin`, performs a deterministic byte-level transformation, and writes the result to `stdout`.
2. Recreate this obfuscator exactly using **Rust**. 
3. Initialize a new Rust project at `/home/user/rust_obfuscator`. 
4. Write the equivalent logic in `/home/user/rust_obfuscator/src/main.rs` and compile it in release mode so the final executable resides at `/home/user/rust_obfuscator/target/release/rust_obfuscator`. 

Your Rust implementation must be functionally bit-exact to the original `/app/c2_obfuscator` binary for any arbitrary binary input. An automated verification system will extensively fuzz both programs with random inputs to ensure identical outputs and exit codes.