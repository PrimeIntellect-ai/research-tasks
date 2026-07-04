We have a critical Bash-based data processing pipeline that orchestrates a math engine, but the system is completely broken after a botched server migration. You need to diagnose and fix several issues across the stack.

Here is the current state of the system in `/app/`:
1. **Deleted Configuration**: A crucial file, `weights.cfg`, was accidentally deleted from `/app/`. However, a background monitoring process was started before the deletion and is still tailing the file. You must recover the exact contents of this file and restore it to `/app/weights.cfg`.
2. **Build Failure**: We vendored a command-line tool called `libmatrix` at `/app/libmatrix-0.9/`. If you try to compile it by running `make` in that directory, it fails with linker errors. Diagnose the compiler/linker error, fix the `Makefile`, and successfully build the `libmatrix` executable.
3. **Concurrency and Numerical Bugs**: The main orchestration script is `/app/process_logs.sh`. It is supposed to read an input log file (passed as the first argument), process each line concurrently using `libmatrix` and the `weights.cfg` file, and output the total sum of the results. 
   - Currently, if you run it, the script deadlocks and hangs forever waiting on background processes.
   - Even when the hang is bypassed, it produces the wrong mathematical answer due to numerical instability and truncation issues in how Bash handles arithmetic. 

Your task:
- Recover `/app/weights.cfg`.
- Fix the `Makefile` and compile `/app/libmatrix-0.9/libmatrix`.
- Debug and modify `/app/process_logs.sh` so that it safely processes lines concurrently without deadlocking, correctly invokes `./libmatrix`, and computes the exact floating-point sum of all outputs (printed to standard output to 6 decimal places).

Your fixed `/app/process_logs.sh` must be robust. An automated testing suite will fuzz your script by passing random input logs and comparing its standard output bit-for-bit against our proprietary oracle reference implementation.