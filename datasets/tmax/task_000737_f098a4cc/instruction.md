As a network engineer inspecting recent traffic logs, you've identified a persistent threat actor targeting our web infrastructure. They are bypassing our traditional WAF by using a custom encoding scheme to obfuscate their XSS and SQL Injection payloads. 

During an investigation of a compromised staging server, we recovered the threat actor's payload generation tool: a stripped Linux binary located at `/app/custom_encoder`. We have also collected a corpus of raw, intercepted traffic payloads (saved as individual files).

Your task is to build a high-performance Deep Packet Inspection (DPI) filter in C that can decode this traffic and flag malicious payloads. 

Here are your objectives:
1. **Analyze the Binary**: Reverse engineer the stripped binary at `/app/custom_encoder` to deduce the custom encoding algorithm. You may use `objdump`, `gdb`, `ltrace`, `strace`, or treat it as a black-box oracle by feeding it inputs.
2. **Develop the Decoder and Filter**: Write a C program at `/home/user/traffic_filter.c`. This program must:
   - Accept a single command-line argument: the absolute path to a payload file.
   - Read the contents of the file.
   - Implement the *inverse* of the algorithm found in `/app/custom_encoder` to decode the payload into plaintext.
   - Perform a vulnerability analysis on the decoded plaintext to identify Common Weakness Enumeration (CWE) patterns for Injection and XSS (e.g., look for standard SQLi indicators like `OR 1=1`, `UNION SELECT`, and XSS indicators like `<script`, `onerror=`, `javascript:`).
3. **Classification Output**: 
   - If the decoded payload contains malicious XSS or SQLi patterns, your program must print exactly `EVIL` to standard output and exit with code 1.
   - If the decoded payload is benign, your program must print exactly `CLEAN` to standard output and exit with code 0.
   - Do not print any other debugging information to standard output.

We have provided a sample dataset for you to test your filter:
- Benign traffic samples: `/app/corpus/clean/`
- Malicious obfuscated payloads: `/app/corpus/evil/`

Compile your final solution to `/home/user/traffic_filter` using `gcc /home/user/traffic_filter.c -o /home/user/traffic_filter`. Ensure it handles edge cases gracefully, such as invalid file paths or malformed encoded strings.