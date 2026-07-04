You are an open-source maintainer reviewing a Pull Request for a small C utility. The PR introduces a minimal build configuration for constrained environments, but it is currently broken and the CI pipeline is failing. 

The project is located in `/home/user/src`.
The PR is provided as a patch file at `/home/user/pr.patch`.

Your task is to fix the PR and verify the constraints:
1. Apply `/home/user/pr.patch` to the source code in `/home/user/src`.
2. The patch introduces a broken `target_minimal` in the `/home/user/src/Makefile`. Fix the Makefile so that running `make target_minimal` successfully compiles the program into a binary named `util_min`. 
   - The minimal build must use conditional compilation (defining the `MINIMAL_BUILD` macro).
   - The minimal build must NOT link against the math library (`-lm`).
   - The resulting binary must be stripped of symbols (using `strip`) to save space.
3. Write a Bash script at `/home/user/verify.sh` that validates the binary meets our strict constraints. The script must:
   - Check that `util_min` is smaller than 20,480 bytes.
   - Check that `util_min` does NOT dynamically link to `libm.so` (using `ldd`).
   - If both constraints are satisfied, write the exact string `OK` to `/home/user/status.txt`.

Ensure your bash script is executable. Run `make target_minimal` and your `./verify.sh` script to produce the final `/home/user/status.txt` file.