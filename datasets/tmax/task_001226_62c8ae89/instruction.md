You are a security researcher analyzing a suspicious telemetry processing pipeline. The system receives base64-encoded payloads, decodes them, and passes them to a legacy shell script. Recently, the system has been crashing and showing signs of command injection. 

You have three main objectives:

1. **Fix the Vendored Package:**
The base64 decoding library we use, `libb64` (version 1.2), is vendored at `/app/libb64-1.2`. However, the previous maintainer introduced some errors, and it currently fails to compile. You must diagnose and fix the compilation errors in the library's `Makefile` and source code so that it can be built successfully using `make`.

2. **Analyze the Crash Logs:**
Inspect the containerized service's crash logs located at `/var/log/telemetry_crash.log`. Use these logs to deduce the exact nature of the corrupted or malicious input. The legacy script downstream seems to break when the decoded base64 contains certain unexpected characters or shell metacharacters (similar to how some scripts break on filenames with spaces).

3. **Develop a Pre-Filter Sanitizer:**
To protect the downstream legacy script, write a C program at `/home/user/sanitizer.c` that acts as an input filter. 
- The program must accept exactly one argument: the path to a base64 encoded input file (e.g., `./sanitizer /path/to/input.b64`).
- It must read the file and determine if it contains ANY characters outside the safe base64 alphabet (A-Z, a-z, 0-9, +, /, =, \n, \r, and spaces). 
- If the file contains potentially dangerous characters (like shell metacharacters or command injection payloads that you identified from the logs), the program must immediately terminate and return an exit code of `1` (indicating rejection).
- If the file is perfectly clean and safe, it must return an exit code of `0` (indicating acceptance).
- Compile your finished program to `/home/user/sanitizer`.

Your solution will be verified programmatically. We have provided two directories containing test inputs:
- `/app/corpus/clean/`: Contains perfectly valid telemetry data.
- `/app/corpus/evil/`: Contains malicious inputs crafted to exploit the downstream script.

Your `sanitizer` must successfully exit `0` for 100% of the files in the clean corpus, and exit `1` for 100% of the files in the evil corpus.