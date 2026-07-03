You are a network engineer inspecting anomalous traffic on a compromised web server. During your investigation, you discovered an unrecognized, stripped executable at `/app/c2_decoder` that the attacker left behind. 

Your analysis of the system's security logs and packet captures suggests that the attacker uses this binary to decode encoded, seemingly benign payloads into active command injections and XSS vectors targeting our backend administrative panels.

Your task is to reverse-engineer the behavior of this stripped binary and write a clean, pure-Bash equivalent tool. This is required because we need to deploy the decoder to our lightweight, embedded edge routers (which lack external libraries, Python, or Perl) to parse security logs in real-time and block malicious payloads automatically.

Requirements:
1. Analyze `/app/c2_decoder`. You may use standard CLI tools (e.g., `strings`, `strace`, `hexdump`, `objdump`, or black-box testing by feeding it inputs) to deduce its encoding/decoding algorithm.
2. Implement the exact same decoding algorithm in a pure-Bash script at `/home/user/edge_decoder.sh`. 
3. Your script must accept a single command-line argument (the encoded payload string) and print the strictly decoded output to standard out, exactly matching the output of the `/app/c2_decoder` binary for the same input.
4. Your script must only use Bash built-ins, coreutils, and standard POSIX shell tools (like `sed`, `awk`, `tr`, `grep`, `printf`). Do not use Python, Ruby, or Perl.
5. Make sure your script is executable (`chmod +x /home/user/edge_decoder.sh`).

The automated test will verify your script by generating hundreds of random encoded payloads and feeding them to both `/app/c2_decoder` and your script to ensure bit-exact output equivalence.