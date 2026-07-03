You are stepping in for a DevOps engineer who was investigating a severe issue with a legacy C-based text processing service. The service has been exhibiting two critical problems: it slowly leaks memory, and occasionally, it completely hangs and stops processing new inputs (CPU usage spikes to 100%).

Before the engineer went on leave, they accidentally deleted the core file `processor.c` and left the codebase in a broken state. 

Your objectives are to completely fix the service by completing the following steps:

1. **Recover the source file**: The deleted `processor.c` still exists in a raw data dump located at `/home/user/backup.img`. The C code is completely encapsulated between the lines `// --- BEGIN PROCESSOR.C ---` and `// --- END PROCESSOR.C ---`. Extract this code and save it to `/home/user/processor.c`.

2. **Fix Compiler/Linker Errors**: The main entry point is at `/home/user/server.c`. Try to compile the program using `gcc /home/user/server.c /home/user/processor.c -o /home/user/server`. You will encounter a linker error. Diagnose the issue and modify `server.c` or `processor.c` to fix it. 

3. **Identify the Hang**: The compiled service reads lines from standard input. Write a bash-only fuzzer (using standard shell tools) or perform code analysis to find the specific input pattern that causes the service to enter an infinite loop. Once identified, write an example string that triggers this exact infinite loop into `/home/user/poison_pill.txt`.

4. **Fix the Bugs (Memory Leak & Loop)**: Inspect `/home/user/processor.c` to locate and fix:
   - The memory leak occurring during input processing.
   - The logical error causing the infinite loop (ensure it safely terminates without hanging, even on malformed inputs).

5. **Final Compilation**: Save your fixed files. Recompile the final, bug-free application to `/home/user/server_fixed` using the same `gcc` command.

**Verification requirements**:
- The recovered `processor.c` must compile alongside `server.c`.
- `/home/user/poison_pill.txt` must contain a string that triggered the hang in the *original* unpatched code.
- `/home/user/server_fixed` must compile successfully, have no memory leaks when run under `valgrind`, and correctly process (without hanging) the contents of `poison_pill.txt`.
- Do not change the overall intended behavior or output messages of `process_input()`.