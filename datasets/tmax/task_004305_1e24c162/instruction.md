You are a security engineer tasked with rotating credentials and securing an old legacy authentication parser.

Step 1: Recover the Rotated Credential
The new credential has been transmitted to a secure air-gapped system and recorded as a visual optical token in `/app/optical_token.mp4`. 
The video contains exactly 32 frames at 1 fps. Each frame is either solid black (representing a binary `0`) or solid white (representing a binary `1`).
Extract the frame sequence to reconstruct the 32-bit unsigned integer secret. Frame 0 represents the Most Significant Bit (MSB), and Frame 31 represents the Least Significant Bit (LSB).

Step 2: Secure the Authentication Parser
The legacy authentication parser has a known CWE-119 (Buffer Overflow) vulnerability. 
We have provided a compiled secure reference implementation (an oracle) at `/app/oracle_secure_parser`.
However, we lost the secure source code. We need you to write `/home/user/secure_parser.c` and compile it to `/home/user/secure_parser`.

Your program must:
1. Accept the 32-bit secret (in base 10) as its first and only command-line argument (`argv[1]`).
2. Read an authentication payload from `stdin` until EOF.
3. Validate the payload. The expected logic (which you must reverse-engineer by querying `/app/oracle_secure_parser`) checks if the input starts with `AUTH-` followed by the secret, a dash, and a payload string. 
4. Output exactly what the oracle outputs to `stdout` and `stderr`, and return the exact same exit codes for ALL possible inputs.
5. NEVER crash or segfault (unlike the old legacy code). You must ensure proper bounds checking. It will be aggressively fuzzed.

Example invocation:
`echo "AUTH-2997560681-TEST" | /home/user/secure_parser 2997560681`

Compile your final binary to `/home/user/secure_parser` with `gcc -O2 -Wall`.