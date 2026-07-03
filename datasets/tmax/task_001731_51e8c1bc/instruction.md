I am migrating a legacy data processing pipeline from Python 2 to Python 3. The pipeline includes a Python script that calls a small C utility to calculate a custom checksum. Currently, the system is broken in several ways: the C utility's Makefile is misconfigured, the Makefile lacks support for a required conditional build flag, and the Python script relies on deprecated Python 2 syntax and string/bytes handling behavior.

Your task is to fix the pipeline. The code is located in `/home/user/legacy/`.

Here are the requirements:

1. **Fix the Makefile:**
   The `Makefile` at `/home/user/legacy/Makefile` is broken (you'll get errors if you try to run `make`). Fix the syntax errors. 
   Additionally, modify it to support conditional builds: if the user runs `make ALT=1`, the compilation must pass the `-DALT_POLY` flag to `gcc`.

2. **Translate Python 2 to Python 3:**
   The script `/home/user/legacy/validator.py` is written in Python 2. 
   Translate it to valid Python 3. Fix any `print` statements, `xrange` usage, and ensure that the subprocess output is properly decoded from bytes to string so it can be parsed as an integer.

3. **Execute and Save the Output:**
   Once fixed, perform the following steps to verify:
   a. Compile the C program using the alternative polynomial logic by running `make ALT=1` inside `/home/user/legacy/`.
   b. Run the migrated Python 3 script with the input string exactly as: `"MigrationTest2023"`
   c. Save the standard output of the Python script to `/home/user/result.txt`.

Ensure the final output file `/home/user/result.txt` contains exactly the output from the Python script. Do not add any extra text to this file.