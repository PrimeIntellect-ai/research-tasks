You are a platform engineer responsible for maintaining the CI/CD pipelines for a Web Security product. We have a C-based authentication helper tool that runs as a lightweight CGI binary. For security and compatibility, we cross-compile this tool for both `x86_64` and `aarch64` architectures. 

Currently, the CI pipeline is broken. The `Makefile` has syntax errors, and we lack an automated way to verify that developers haven't accidentally compiled debug features into the production binaries.

Your task is to fix the build step and write a Python tool to enforce symbol allowlisting:

1. **Fix the Build:**
   Navigate to `/home/user/build/`. You will find `auth_helper.c` and a broken `Makefile`. Repair the `Makefile` so that running `make all` successfully cross-compiles the code, producing two binaries: `auth_x86` and `auth_arm`. (The system already has `gcc` and `aarch64-linux-gnu-gcc` installed).

2. **Create the CI Check Script:**
   Write a Python script at `/home/user/build/ci_check.py` that takes a binary file path as a command-line argument. The script must:
   - Execute the standard `nm` command on the provided binary.
   - Parse the output to find all global text symbols (indicated by the letter `T` in `nm` output).
   - Filter this list to only include symbols that begin with the prefix `websec_`.
   - Sort the resulting symbol names alphabetically.
   - Read the allowed symbols from `/home/user/build/expected_symbols.txt`.
   - Perform a diff: identify any `websec_` symbols present in the binary that are *not* present in `expected_symbols.txt`.

3. **Generate the Security Reports:**
   Run your script on both compiled binaries. If any unauthorized symbols are found, append them to a log file named `/home/user/build/security_violations.log`. The file should contain one symbol name per line. If the exact same unauthorized symbol appears in both binaries, it should appear twice in the log file (once for each binary check).

Ensure your final output log `/home/user/build/security_violations.log` exists and contains exactly the extracted anomalous symbols.