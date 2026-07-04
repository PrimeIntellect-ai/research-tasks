You are an on-call engineer who just received a 3 AM page. The primary data processing service `/home/user/processor` has crashed in production. 

Here is what you have:
1. The source code of the service: `/home/user/processor.c`
2. The compiled binary: `/home/user/processor`
3. A core dump generated at the time of the crash: `/home/user/core`
4. The service log file: `/home/user/service.log`

The log file contains multiple requests processed by the server tonight. Each log line includes a timestamp, a transaction ID, and a base64-encoded payload.

Your objectives:
1. **Core Dump & Log Analysis**: Analyze the core dump to determine which specific transaction caused the crash. Extract the corresponding base64 payload from `/home/user/service.log` and decode it.
2. **Delta Debugging (Minimization)**: The original payload that caused the crash is quite large. Write a script to minimize this decoded payload to the absolute shortest byte sequence that still causes `/home/user/processor` to exit with a Segmentation Fault (SIGSEGV). Save this minimal crashing payload to `/home/user/minimal_crash.bin`.
3. **Root Cause Fix**: Identify the bug in `/home/user/processor.c` that causes the buffer overflow. Fix the code to safely handle large inputs without truncating valid data (reallocate dynamically or safely reject if that's the program's logic, but ensure it no longer crashes). Save the fixed source code to `/home/user/processor_fixed.c`.

Constraints:
- The minimal crashing payload in `/home/user/minimal_crash.bin` must be the strict minimum number of bytes required to trigger the crash.
- Ensure your fixed code compiles cleanly with `gcc -g -fno-stack-protector -O0 /home/user/processor_fixed.c -o /home/user/processor_fixed`.