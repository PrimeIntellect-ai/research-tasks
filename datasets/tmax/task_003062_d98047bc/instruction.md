You are a forensics analyst investigating a compromised Linux web server. The attacker successfully exfiltrated sensitive web administration logs by hiding them inside a seemingly innocuous audio file left on the server. You need to extract the evidence, analyze the attacker's privilege escalation vector, and safely analyze a leftover malware payload.

Complete the following objectives using C as your primary implementation language:

1. **Evidence Extraction (Audio Steganography):**
   The attacker encoded a captured HTTP traffic log into `/app/exfil_audio.wav`. They used basic Least Significant Bit (LSB) steganography. Specifically, the lowest bit of each 16-bit PCM audio sample (little-endian sample order) forms the bits of the hidden ASCII characters (8 bits per byte, constructed from the LSBs in little-endian bit order, meaning the first audio sample's LSB is the least significant bit of the first character).
   Write a C program, `/home/user/extract.c`, that reads the WAV file, extracts the hidden message, and writes the resulting text to `/home/user/recovered_traffic.log`. Stop extracting when you hit a null terminator (`\0`).

2. **HTTP Header and Cookie Inspection:**
   The extracted text in `/home/user/recovered_traffic.log` contains raw HTTP requests. Analyze these logs to identify the exact HTTP `Cookie` header string that the attacker used to bypass authentication and achieve privilege escalation. Save this exact string (e.g., `Cookie: session_id=...`) to `/home/user/malicious_cookie.txt`.

3. **Process Isolation and Sandboxing:**
   You have discovered a suspicious binary left by the attacker at `/app/backdoor_probe`. To safely analyze what it attempts to do without risking further compromise to your system, write a C program at `/home/user/sandbox.c` that uses `seccomp-bpf` or `libseccomp` to strictly isolate the execution of `/app/backdoor_probe`.
   Your sandbox must:
   - Fork and execute `/app/backdoor_probe`.
   - Restrict the child process so it is ONLY allowed to make the following syscalls: `read`, `write`, `exit`, `exit_group`, `brk`, `mmap`, `munmap`, and `execve`.
   - If the binary attempts ANY other syscall (like `socket` or `open`), the process must be immediately killed by the kernel (`SECCOMP_RET_KILL`).
   Capture the standard output of the sandboxed binary execution and save it to `/home/user/sandbox_output.txt`.

Ensure your C code compiles cleanly. Your extraction tool's accuracy will be quantitatively measured.