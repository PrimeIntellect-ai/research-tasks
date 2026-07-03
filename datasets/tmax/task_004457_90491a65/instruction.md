You are a forensics analyst investigating a compromised Linux host. The attacker has exfiltrated data by embedding encoded payloads into the system logs to evade network-level Data Loss Prevention (DLP) systems.

We have isolated a suspicious stripped ELF binary left by the attacker at `/app/exfil_decoder`, and a copy of the compromised system's log file at `/home/user/syslog`.

Your objective is to recover the stolen data and expose it securely for our incident response automated collection system.

Phase 1: Log Parsing and Correlation
The attacker's payloads are hidden in `/home/user/syslog` within lines containing the string `[SYSTEM_ALERT_909]`. 
Extract the hex-encoded payload strings from these specific log lines. The payloads are fragmented and must be processed in the exact order they appear in the log file.

Phase 2: Binary Analysis and Payload Decoding
The binary `/app/exfil_decoder` was used by the attacker. It is a stripped binary. Through reverse engineering or black-box analysis, you must determine how to use this binary to decode the hex payloads extracted in Phase 1. 
Hint: The binary expects a secret key to authorize decryption. You will need to analyze the binary (e.g., using `strings`, `ltrace`, `strace`, or `objdump`) to discover this hardcoded key and the correct command-line arguments to pass the hex payloads for decryption. 

Phase 3: Evidence Hosting (C2 Emulation)
Once you have decoded all fragments, concatenate them in their original order to reconstruct the complete exfiltrated data.
You must then write a pure Bash script (using tools like `nc`, `awk`, or bash built-ins; do NOT use Python, Node, etc.) that starts a TCP server listening on port `8080`.
This server must implement the following custom text-based protocol to serve the evidence to our automated collection system:
1. When a client connects and sends the exact string `HELO`, the server must respond with `ACK`.
2. When the client subsequently sends `GET_EVIDENCE`, the server must respond with the fully reconstructed plaintext data, followed by a newline, and then close the connection.

Run your server in the background so it is ready to receive requests.

Constraints:
- You must use Bash and standard Linux command-line utilities.
- The server must listen on `127.0.0.1:8080`.