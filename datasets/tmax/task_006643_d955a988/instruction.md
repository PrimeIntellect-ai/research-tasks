You are an engineer tasked with maintaining a long-running mathematical service that calculates the roots of high-degree polynomials over many iterations. The service has been experiencing severe memory leaks, eventually crashing due to OOM (Out of Memory) errors. 

To make matters worse, a junior developer accidentally deleted the critical source file `poly_math.c` and ran a destructive git command (`git reset --hard` and wiped the commit), removing it from the working tree and branch history.

Your task is to fully restore the service, fix the compilation issues, and resolve the memory leak.

Here are your detailed instructions:
1. Navigate to the repository at `/home/user/service_repo`.
2. Recover the deleted file `poly_math.c`. The file contents are still in the Git database as a dangling blob. Find the blob and restore it exactly as `poly_math.c` in the repository root.
3. The recovered file will not compile with `main.c` due to missing standard headers and a missing mathematical library flag during linking. Fix the source code of `poly_math.c` so it compiles successfully without warnings, and figure out the correct `gcc` compilation command to produce an executable named `math_service`.
4. The service currently has a severe memory leak in `poly_math.c`. Use a debugger or memory analysis tool (like `valgrind` or `gdb`) to identify where memory is being allocated but not freed.
5. Fix the memory leak in `poly_math.c`. You must ensure that the program logic remains exactly the same—only add the necessary memory management code (e.g., `free()`) to prevent the leak.
6. Recompile the fixed code into `math_service`.
7. Run `./math_service`. It will automatically process 10,000 iterations and write its output to `/home/user/service_repo/results.txt`.
8. Create a log file at `/home/user/leak_report.txt`. In this file, write exactly the line number of the original `poly_math.c` (as recovered from the Git blob) where the leaked memory was originally allocated (e.g., "Line: 42").

Verification Criteria:
- `/home/user/service_repo/poly_math.c` must exist, compile without errors, and have no memory leaks.
- `/home/user/service_repo/math_service` must be a compiled executable.
- `/home/user/service_repo/results.txt` must contain the final expected mathematical output.
- `/home/user/leak_report.txt` must contain the correct line number of the original allocation.
- Running `valgrind --leak-check=full ./math_service` must report "0 bytes in 0 blocks" for "definitely lost".