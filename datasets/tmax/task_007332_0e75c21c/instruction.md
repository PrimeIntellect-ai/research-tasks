You are an on-call engineer responding to a 3 AM page. A critical legacy monitoring service has stalled. The service is run by a background script named `legacy_monitor.sh`. 

This script generates a temporary C source file, opens a file descriptor to it, attempts to compile it, and then instantly deletes the source file to clean up. However, the compilation is failing, and the script is now hanging indefinitely, though it still holds the deleted C file open.

Your task is to investigate and resolve this issue:
1. **Recover the source code**: Inspect the running `legacy_monitor.sh` process, find the deleted C file it is holding open, and recover its contents to `/home/user/recovered.c`.
2. **Fix the compilation**: Attempt to compile `/home/user/recovered.c` into an executable named `/home/user/app.bin` using `gcc`. You will encounter an error (a linker error). Interpret this error and provide the correct flags to successfully compile the binary. *Note: Ensure you compile with `-fno-stack-protector` so that memory corruptions manifest as raw segmentation faults.*
3. **Trace the crash**: The recovered C program contains a buffer overflow vulnerability that only manifests with specific input lengths. Using a bash script or system call tracing tools (like `strace`), find the *shortest* string consisting entirely of the uppercase letter `A` (e.g., "AAAA...") that causes `/home/user/app.bin` to crash with a Segmentation Fault (SIGSEGV / exit code 139). 
4. Write this exact crash-inducing string of 'A's to `/home/user/crash_payload.txt`.

System state requirements for success:
- `/home/user/recovered.c` must contain the exact recovered source code.
- `/home/user/app.bin` must be a compiled, runnable binary of the recovered code.
- `/home/user/crash_payload.txt` must contain only the 'A's payload that triggers the segfault.