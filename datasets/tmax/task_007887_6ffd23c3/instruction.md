You are a security researcher analyzing a suspicious Rust-based malware dropped on a compromised machine. The malware source code has been partially recovered, along with a network packet capture of its communication with a Command & Control (C2) server.

Your objective is to:
1. Fix the build failure in the recovered malware source code located at `/home/user/c2_agent`.
2. Analyze the network capture at `/home/user/capture.pcap`. Identify the TCP packet destined for port 1337 and extract its payload.
3. The malware binary takes a file path as its first argument (e.g., `./target/debug/c2_agent payload.bin`). It reads the file and looks for a specific instruction. If it finds it, it prints `[!] C2 INSTRUCTION RECEIVED`.
4. The payload extracted from the pcap triggers this message, but it contains a lot of junk data. You must use delta debugging/test minimization techniques to find the **absolute shortest contiguous byte sequence** from the extracted payload that still causes the malware to print `[!] C2 INSTRUCTION RECEIVED`.
5. Write this exact minimal byte sequence as a continuous lowercase hexadecimal string (e.g., `aabbccddeeff`) into the file `/home/user/minimal_trigger.txt`.

Constraints:
- Do not modify the logic of the malware in `/home/user/c2_agent/src/main.rs` other than fixing the compilation error. 
- You may use any shell tools or write your own Rust/Python scripts to parse the pcap, extract the payload, and automate the minimization.
- The final answer in `/home/user/minimal_trigger.txt` must contain ONLY the hexadecimal string and no other text or newlines.