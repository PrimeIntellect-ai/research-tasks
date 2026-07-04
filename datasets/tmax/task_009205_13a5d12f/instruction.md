You are a network engineer tasked with investigating suspicious traffic targeting a custom internal service. You have been provided with the source code of the service and a hex dump of the intercepted traffic.

Files provided:
1. `/home/user/src/service.c` - The source code for the custom TCP service running on port 8888.
2. `/home/user/traffic_dump.txt` - A hex dump of the intercepted malicious payload sent to the service.

Your objectives:
1. **Vulnerability Analysis:** Analyze `/home/user/src/service.c` to identify the vulnerability being exploited. Create a file named `/home/user/analysis.txt`.
   - On Line 1, write the exact name of the vulnerable C function.
   - On Line 2, write the exact size (in bytes) of the buffer that is being overflowed.

2. **Process Isolation (Sandboxing):** To mitigate future exploits while the developers patch the code, you must write a seccomp-BPF wrapper in C.
   - Create the source file at `/home/user/sandbox.c`.
   - The program should accept one or more command-line arguments representing a program to execute and its arguments (e.g., `./sandbox ./src/service`).
   - The program must use the `prctl` system call to set `PR_SET_NO_NEW_PRIVS`.
   - The program must install a seccomp-BPF filter that allows all system calls EXCEPT `execve` and `execveat`. If `execve` or `execveat` is called, the filter should kill the process (e.g., return `SECCOMP_RET_KILL_PROCESS` or `SECCOMP_RET_KILL`).
   - After applying the filter, the program must execute the provided command using `execvp`.
   - Compile your wrapper to `/home/user/sandbox`. Ensure it is executable.

Note: You can use the `linux/seccomp.h` and `linux/filter.h` headers. Ensure your wrapper does not block the initial `execvp` that launches the service; you may need to apply the filter *after* forking, or design the BPF filter to only block `execve` if it is called *after* the initial binary execution (or simply let the wrapper fork, apply seccomp in the child, and then exec the service - wait, if you apply seccomp before exec, the `execvp` to start the service will be blocked! Think carefully about how to structure the BPF filter or execution flow so the service itself can run, but any *subsequent* shellcode executing `execve` will be killed). 
*Hint*: A common pattern is to write a filter that blocks `execve`, fork, apply the filter in the child, and then wait, you can't `execve` after blocking it. Alternatively, write the seccomp wrapper as a shared library injected via `LD_PRELOAD` that applies the filter in a constructor *after* the binary has loaded, or compile the seccomp filter directly into a patched version of `service.c`.
Actually, to make it verifiable and straightforward: Patch `/home/user/src/service.c` directly to include a function `void apply_sandbox()` called at the very beginning of `main()`. The function must install the seccomp filter blocking `execve` and `execveat`. Compile the patched service to `/home/user/service_secured`.

Output requirements:
- `/home/user/analysis.txt` as specified.
- The patched C source code at `/home/user/src/service.c` with the `apply_sandbox()` function.
- The compiled executable at `/home/user/service_secured`.