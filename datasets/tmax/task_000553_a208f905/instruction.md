You are a DevSecOps engineer tasked with enforcing policy as code for a legacy C-based file upload handler that recently suffered a path traversal breach. You need to analyze the incident, reverse-engineer a newly approved sanitization policy, and implement a replacement sanitizer.

Phase 1: Incident Analysis (Video)
An intrusion was recorded in a screen capture at `/app/incident_record.mp4`. 
1. Use `ffmpeg` to extract frames from this video.
2. Analyze the frames to identify the exact malicious HTTP `Upload-Path` value used in the attack.
3. Determine the standard CWE ID for the vulnerability exploited (Path Traversal).
4. Create a log file at `/home/user/policy_report.txt` with exactly two lines:
   - Line 1: The exact raw malicious `Upload-Path` payload extracted from the video.
   - Line 2: The CWE ID (in the format `CWE-XXX`).

Phase 2: Policy Reverse Engineering (ELF Analysis)
The security team has provided a stripped reference binary at `/app/sanitizer_oracle`. This binary implements the strict sanitization policy for the `Upload-Path` header. 
1. Analyze this ELF binary to understand its exact sanitization logic. 
2. The binary reads a raw HTTP request from standard input (stdin).
3. It extracts the value of the `Upload-Path` HTTP header.
4. It applies a specific transformation/sanitization routine to neutralize path traversals and URL encoding.
5. It prints ONLY the final sanitized path to standard output (stdout), with no trailing newline.

Phase 3: Implementation
1. Write a C program at `/home/user/sanitizer.c`.
2. The program must replicate the exact behavior of the `/app/sanitizer_oracle`.
3. It must read a raw HTTP request from stdin, parse the `Upload-Path` header, sanitize it identically to the oracle, and output the result to stdout.
4. Compile your program to `/home/user/sanitizer` using `gcc -O2 /home/user/sanitizer.c -o /home/user/sanitizer`.

Your final compiled binary must be BIT-EXACT equivalent to the oracle in its input/output behavior. An automated fuzzer will test your `/home/user/sanitizer` against `/app/sanitizer_oracle` with thousands of randomized HTTP requests containing complex path traversal payloads.