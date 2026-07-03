You are acting as a penetration tester and security engineer. We have discovered a vulnerable stripped binary, `/app/vuln_server`, which is a custom web service. It has been crashing periodically in production due to malformed HTTP requests containing specific exploit payloads.

Your goal is twofold:
1. **Reverse Engineering & Exploit Analysis**: Analyze the stripped binary `/app/vuln_server` using standard reverse engineering tools (e.g., `objdump`, `gdb`, `strings`) to determine the exact nature of the vulnerability. The crash is known to occur during the parsing of HTTP headers and cookies. Find out what specific input triggers the memory corruption.
2. **Sanitizer Development**: Write a C program that inspects incoming HTTP requests and reliably detects the exploit payload without blocking legitimate traffic.

**Requirements for the Sanitizer:**
- Create your source code at `/home/user/sanitizer.c`.
- The program must take a single command-line argument: the path to a file containing a raw HTTP request.
- Parse the HTTP headers and cookies to enforce content security rules based on your reverse-engineering findings.
- If the HTTP request contains the exploit payload (i.e., it would trigger the vulnerability in `/app/vuln_server`), the program must print exactly `EVIL` to standard output and exit with status code `1`.
- If the HTTP request is benign, the program must print exactly `CLEAN` to standard output and exit with status code `0`.
- Your program must be able to be compiled with `gcc -O2 /home/user/sanitizer.c -o /home/user/sanitizer`.

To succeed, you must correctly reverse-engineer the logic, write robust C code to parse HTTP requests, and successfully classify requests. An automated test suite will compile your code and run it against a hidden corpus of both clean and malicious requests.