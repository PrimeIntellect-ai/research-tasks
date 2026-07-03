You are a DevOps engineer responsible for maintaining a legacy C-based log parsing utility. 

We have the source code for the `parseman` utility (version 1.0) located in `/app/parseman-1.0`. This utility parses our custom binary log format. However, we are facing a few issues:

1. **Build Failure**: The project currently fails to build. Diagnose the build failure in `/app/parseman-1.0` and fix it so that running `make` successfully produces the `parseman` executable.
2. **Crash Analysis**: The `parseman` binary is known to crash (segmentation fault) when processing certain malformed logs. You need to figure out exactly what malformed data causes this crash. You are encouraged to write a simple fuzzer or manually craft inputs to reproduce the crash. Ensure that core dumps are enabled (`ulimit -c unlimited`) so you can analyze the crash using `gdb` and stack traces. The binary expects log files to start with the magic bytes `L0GZ`, followed by a series of TLV (Type-Length-Value) records. The length field is 2 bytes, little-endian.
3. **Log Sanitiser**: Once you understand the vulnerability, write a standalone C program at `/home/user/detector.c` that detects whether a given log file contains the malicious payload that would crash `parseman`. 
   - Compile your program to `/home/user/detector`.
   - Your program must accept exactly one argument: the path to the log file to analyze (e.g., `./detector /path/to/log.bin`).
   - If the log file contains the malformed data that triggers the specific buffer overflow in `parseman`, your program MUST exit with code `1`.
   - If the log file is clean and safe to process, your program MUST exit with code `0`.

You must leave the final working source code at `/home/user/detector.c` and the compiled binary at `/home/user/detector`. An automated verification script will test your detector against two hidden corpora of logs (one containing perfectly clean logs, and another containing malformed, "evil" logs that trigger the crash). Your detector must correctly classify 100% of the logs in both corpora.