You are tasked with investigating a memory leak in a C-based transaction processing service. The service parses hex-encoded payloads, decodes them, and processes them. A specific type of malformed transaction is causing an early exit in the processing function, leading to a memory leak. 

The source code for the service is located at `/home/user/service/`.
The build system is a simple Makefile. You can compile the service by running `make` in that directory. The resulting executable is `tx_service`.

Your objectives are:
1. **Identify and Fix the Leak:** Inspect `/home/user/service/tx_proc.c`. Find the logical flow that causes the memory leak (an early return failing to free the decoded buffer). Write a fix for this memory leak.
2. **Generate a Patch:** Create a unified diff (using `diff -u`) of your modified `tx_proc.c` against the original file (which you should back up before editing). Save this patch to `/home/user/fix.patch`. The patched code must compile and run cleanly under Valgrind with 0 bytes leaked.
3. **Extract the Leaked Payload:** The `main.c` file runs a series of hardcoded encoded transactions. One of them triggers the leak. By running the program in `gdb`, using `valgrind`, or analyzing the memory, identify the *decoded* string of the payload that leaked. The leaked decoded string will begin with `ERR_TX_`. Write this exact decoded string to `/home/user/leaked_tx.txt`.

Ensure your patch cleanly applies and correctly frees the memory without causing double-free or use-after-free errors.