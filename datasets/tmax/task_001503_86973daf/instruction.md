You are a network engineer inspecting encrypted traffic and building a security analysis tool. We have intercepted a dashboard visualization video at `/app/traffic_monitor.mp4` and need you to extract the hidden data and build a traffic filter in Rust.

**Part 1: Video Analysis**
The video `/app/traffic_monitor.mp4` (Resolution: 1280x720) flashes 8 black and white squares across the top of the video (from y=0 to y=160). Each square is 160x160 pixels.
- Each frame of the video encodes exactly 1 byte.
- The 8 squares represent the 8 bits of the byte, with the Most Significant Bit (MSB) on the left (x=0) and the Least Significant Bit (LSB) on the right (x=1120).
- A white square (average pixel value > 128) represents a `1` bit. A black square (average pixel value < 128) represents a `0` bit.
- Extract the byte stream from all frames of the video and save the resulting ASCII string to `/home/user/secret_key.txt`.

**Part 2: Security Log Analyzer in Rust**
We need a high-performance log analyzer to process incoming traffic.
Initialize a Rust binary project at `/home/user/log_analyzer` (e.g., using `cargo new`).
Write the code in `src/main.rs`. We will compile and test it.

The program must read log lines from `stdin` (standard input) one by one and write the decision to `stdout`.
For each line, apply the following rules in this **exact order**:
1. **TLS Check**: If the line does NOT contain the exact substring `[TLS:OK]`, print `DENY: Invalid TLS`.
2. **XSS Vulnerability Analysis**: If the line contains `<script>` or `javascript:`, print `DENY: XSS detected`.
3. **Injection Analysis**: If the line contains `' OR ` or `UNION SELECT`, print `DENY: SQLi detected`.
4. **Access Control / Privilege Escalation**: The username is the first space-separated word on the line. If the username is exactly `root` or `admin`, print `DENY: Privilege escalation`.
5. **Default Secure**: If none of the above violations are found, print `ALLOW`.

Ignore completely empty lines. Your program's output will be fuzzed for BIT-EXACT equivalence against a reference oracle binary. Ensure you follow the rules and ordering perfectly.