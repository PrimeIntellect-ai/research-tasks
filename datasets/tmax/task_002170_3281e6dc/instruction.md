You are a DevOps engineer debugging a legacy log processing utility written in C. The utility, located at `/home/user/log_processor/parser.c`, reads a file containing comma-separated mathematical calculations and outputs a final sum. However, the program is currently failing to run, and when forced to run, it segfaults on corrupted production logs.

Your task is to fix the environment and the code to successfully process `/home/user/log_processor/data.log`.

Perform the following steps:
1. The compiled program (`/home/user/log_processor/log_calc`) silently exits with an error code before printing anything. Use system call tracing to discover which authentication key file the program is trying to open, and where it expects it to be located.
2. The expected contents of this authentication key file were accidentally committed to the git repository in the past, but were subsequently removed. Use git history forensics to recover the secret key string.
3. Create the required key file at the exact path the program expects, containing only the recovered secret key.
4. Once the program can start, you will notice it crashes (Floating point exception or Segmentation fault) when processing `data.log`. Inspect `parser.c` and fix the format parsing logic. 
   - Modify the code to safely handle corrupted inputs by verifying the parser successfully extracts exactly three integers per line. Skip any malformed lines.
   - The program performs division using the third integer. Modify the logic to skip lines where the third integer is zero.
   - Add an `assert()` statement right before the division operation to explicitly validate that the divisor is not zero (assertion-based intermediate validation).
5. Compile your fixed C code: `gcc -o /home/user/log_processor/log_calc /home/user/log_processor/parser.c`
6. Run the compiled program, passing `/home/user/log_processor/data.log` as the first argument.
7. Redirect the standard output of the successful run to `/home/user/final_result.txt`.

Ensure `/home/user/final_result.txt` contains exactly the output printed by the fixed program.