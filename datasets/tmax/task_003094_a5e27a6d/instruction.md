You are a network engineer investigating an incident where suspicious traffic was observed on your network. During the investigation, you recovered an unknown executable binary dropped by an attacker. It is located at `/home/user/traffic_analyzer`. 

Your goal is to reverse engineer this binary to understand its custom authentication and payload processing mechanisms. Based on your analysis, you must write a C++ program that can generate a valid authentication token and identify the hardcoded backdoor injection payload.

Perform the following steps:
1. Analyze the ELF binary `/home/user/traffic_analyzer` (e.g., using `objdump`, `gdb`, `strings`, or other tools) to understand how it validates the first command-line argument (the token) and checks the second command-line argument (the payload).
2. The binary implements a custom cryptographic checksum for the token and checks for a specific SQL injection string that acts as a backdoor.
3. Write a C++ program at `/home/user/generate_report.cpp`. When compiled and executed, this program must generate a valid token that satisfies the binary's token validation logic, and it must output the exact backdoor SQL injection string found in the binary.
4. Your C++ program must write its output to `/home/user/report.txt` in the following exact format:
```
TOKEN: <valid_token>
BACKDOOR: <the_exact_sql_injection_string>
```

Constraints and hints:
- The binary returns a specific exit code (42) if both the token is valid and the backdoor payload is provided. You can use this to verify your findings.
- You may use any available reverse engineering or binary analysis tools in the terminal.
- Do not hardcode the token in your C++ script by simply guessing; write C++ code that deterministically generates a valid token based on the rules you discover (e.g., matching the required prefix and checksum). However, the backdoor string can simply be printed.
- Compile your C++ program and run it to produce `/home/user/report.txt`.