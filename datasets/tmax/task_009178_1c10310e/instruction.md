You are a QA engineer tasked with setting up and fixing a test environment for a custom Python module that calculates Adler-32 checksums. The module is implemented as a C extension for performance. However, the build configuration is broken, the C implementation has a logical bug, and the test automation script is missing.

Your task consists of the following phases:

1. **Fix the C Extension Bug:** 
   The source code for the extension is located at `/home/user/project/adler32.c`. The Adler-32 algorithm implemented in this file is currently incorrect. Identify the bug (hint: review the modulo constant used in Adler-32) and fix the C code.

2. **Fix the Build System:**
   The build configuration file `/home/user/project/setup.py` is broken and fails to compile the C extension into a module named `adler32_fast`. Fix `setup.py` so that it references the correct source file.

3. **Build the Module:**
   Compile the C extension in-place so it can be imported directly by Python in the `/home/user/project` directory (e.g., using `python3 setup.py build_ext --inplace`).

4. **Write the Test Automation Script:**
   You will find two directories containing test files: `/home/user/project/data_a` and `/home/user/project/data_b`. Both directories contain files with the exact same names.
   Write a Bash script at `/home/user/project/compare.sh` that:
   - Iterates through all files in `data_a`.
   - Uses a short inline Python command to compute the Adler-32 checksum of the file in `data_a` and the corresponding file in `data_b` using the compiled `adler32_fast.checksum(data)` function.
   - Compares the two checksums.
   - Outputs a line for each file in the format: `<filename>: MATCH` if the checksums are identical, or `<filename>: MISMATCH` if they differ.
   
5. **Generate the Final Report:**
   Run your `compare.sh` script, sort the output alphabetically by filename, and save the sorted output to `/home/user/project/comparison_results.txt`.

**Constraints and requirements:**
- Do not use the `zlib` standard library in Python to compute the checksums; you MUST use the compiled `adler32_fast` module.
- The `adler32_fast.checksum()` function expects a single bytes object as an argument and returns an integer.
- The final output in `/home/user/project/comparison_results.txt` must strictly contain only the sorted lines formatted as described above.