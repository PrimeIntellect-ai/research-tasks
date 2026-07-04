Wake up, you're on-call. It's 3 AM and the legacy mathematical network service is crashing in production. 

The service listens for UDP packets and computes the Greatest Common Divisor (GCD) of two 32-bit integers. A malicious or malformed payload has been causing a `SIGFPE` (Floating-Point Exception) core dump. 

Additionally, the incident response team noticed that a junior developer recently committed and then quickly removed a production secret from the Git repository. We need to rotate that secret, but we need to know what it was first.

Your objectives:
1. **Git Forensics**: Navigate to the repository at `/home/user/math_server`. Search the Git history to find the leaked secret. It was added as a comment in the format `// SECRET_KEY=...` and removed in a subsequent commit.
2. **PCAP Analysis**: We captured the packet that caused the crash. Analyze `/home/user/crash.pcap`. It contains a single UDP packet directed to port 8888. The payload consists of exactly two 32-bit signed integers in network byte order (big-endian). Determine what these two integers are.
3. **Fix the Bug**: The code for the math operations is in `/home/user/math_server/math_ops.c`. The `gcd(int a, int b)` function has a mathematical flaw that causes a hardware trap (SIGFPE) on certain specific inputs (like the ones from the pcap). Modify the `gcd` function in `math_ops.c` so that if this specific edge case is encountered, it returns `-1` instead of crashing.
4. **Regression Test**: Create a C program at `/home/user/math_server/test.c` that includes `math_ops.c` and calls `gcd()` with the two integers you extracted from the pcap. The program must return exit code `0` if `gcd` correctly returns `-1`, and exit code `1` otherwise. Compile it to an executable named `/home/user/math_server/run_test`.
5. **Report Generation**: Create a file at `/home/user/resolution.txt` with exactly the following format:
```
SECRET: <the_secret_string>
CRASH_INPUTS: <integer_a>, <integer_b>
```
*(Replace the placeholders with the actual values. integer_a is the first 32-bit integer in the payload, integer_b is the second).*

Ensure the executable `/home/user/math_server/run_test` works and that the resolution file is strictly formatted.