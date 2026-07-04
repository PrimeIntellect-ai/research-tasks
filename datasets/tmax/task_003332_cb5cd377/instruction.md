You are a QA engineer responsible for setting up a low-level CI/CD test environment. Your goal is to write a standalone continuous integration Bash script that builds a minimal program, tests its execution, and performs a mathematical analysis on the compiled binary's data encoding.

Create a single Bash script at `/home/user/build_and_test.sh` that performs the following steps in order when executed:

1. **Assembly Program Construction**: Dynamically generate a minimal x86_64 Linux GNU Assembler file (AT&T syntax) at `/home/user/calc.s`. This assembly program must contain a `_start` entry point and simply exit with the status code `73` using the `sys_exit` syscall.
2. **Build Process**: Use the standard GNU binutils (`as` and `ld`) to assemble `/home/user/calc.s` into an object file and link it into an executable named `/home/user/calc`.
3. **Execution & Verification**: Execute `/home/user/calc` and capture its exit status. Assert that the exit status is exactly `73`. If it is not, the script should exit immediately with a non-zero status.
4. **Data Encoding**: If the exit code is correct, read the entire compiled `/home/user/calc` executable binary and encode it into a continuous, lowercase hexadecimal string containing no spaces or newlines (you can use standard tools like `od` or `hexdump`).
5. **Mathematical Analysis**: Iterate over the resulting hexadecimal string and calculate the mathematical sum of all the numeric digits (`0`-`9`) present in the string. Ignore any alphabetic hex characters (`a`-`f`).
6. **Output Generation**: Write the final calculated integer sum to a file located at `/home/user/math_result.txt`.

Ensure your script is executable. You can run the script yourself in the terminal to verify that `/home/user/math_result.txt` is created with the correct numeric sum. Standard Linux utilities (`as`, `ld`, `od`, bash built-ins) are available in the environment.