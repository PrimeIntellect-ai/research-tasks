You are an open-source maintainer reviewing a pull request for a C++ utility that evaluates simple mathematical expressions and computes a CRC8 checksum of them. The contributor claims the code is complete, but the CI pipeline is failing.

The files are located in `/home/user/pr_review/`. 
You need to fix the repository so that the tests pass. 

Specifically, you must:
1. Fix the `Makefile`. The contributor made a classic mistake in the Makefile formatting that prevents `make` from running.
2. Fix a compilation error in `eval_crc.cpp`.
3. Fix a logical bug in the expression evaluation logic in `eval_crc.cpp`. Currently, it fails to respect the standard order of operations (multiplication `*` should have a higher precedence than addition `+`). The expressions will only contain single-digit integers, `+`, and `*`, with no spaces (e.g., `2+3*4`).
4. Fix a logical bug in the `calculate_crc8` function. The standard CRC8 polynomial used in this project should be `0x07`. The contributor made a typo in the bitwise XOR operation inside the loop.
5. Compile the project using `make`.
6. Run the compiled `./test_runner` executable.
7. Save the standard output of `./test_runner` exactly as it is to `/home/user/test_results.log`.

Do not modify the `test_runner.cpp` or `eval_crc.h` files. Only modify `Makefile` and `eval_crc.cpp`.