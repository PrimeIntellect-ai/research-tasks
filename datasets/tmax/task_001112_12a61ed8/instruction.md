I am a QA engineer setting up a test environment for our web security pipeline. We have a custom C-based log parser that extracts malicious IP addresses and attack types from a structured data stream. However, the parser is failing and crashing when processing our new test logs. 

It seems there might be a memory corruption issue related to how the state machine parses tokens, similar to how unexpected nested configurations can crash dependency resolvers in Node.js projects.

Here is the setup:
- The parser source code is at `/home/user/parse_logs.c`.
- The test log file is at `/home/user/attack_logs.dat`.
- The parser uses a manual state machine to read the colon-separated structured format.

Your task:
1. Use memory debugging techniques (e.g., `gcc -fsanitize=address` or `valgrind`) to identify why `/home/user/parse_logs.c` is crashing.
2. Fix the bug in `/home/user/parse_logs.c`. You should only need to modify a buffer size or add bounds checking in the state machine logic.
3. Compile the fixed code to `/home/user/parse_logs` using `gcc`.
4. Run `/home/user/parse_logs`. It is hardcoded to read `/home/user/attack_logs.dat` and output to `/home/user/malicious_ips.txt`.

Ensure the final output file `/home/user/malicious_ips.txt` is successfully generated and contains the extracted IPs and attack types.