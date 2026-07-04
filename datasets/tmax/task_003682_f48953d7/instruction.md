You are a support engineer tasked with collecting diagnostics and fixing a failing C++ mathematical simulation for a client. The client's workspace is located at `/home/user/sim_project`.

Currently, the project suffers from two major issues:
1. **Build Failure:** Running `make` fails with a linker error. The project relies on a pre-compiled library, but there is a dependency conflict between the library version specified in the `Makefile` and the functions called in the code.
2. **Precision Loss:** Once the build is fixed, running the compiled `./sim` executable produces an `output.csv` file. The client has provided a `baseline.csv` representing the exact expected mathematical results. The current C++ code contains a precision loss bug (e.g., improper casting or use of lower-precision types) that causes the calculated trajectory to accumulate error and diverge from the baseline.

**Your objectives:**

1. **Fix the Linker Error:** Inspect the `Makefile` and the `libs/` directory. Resolve the dependency conflict so that the project compiles successfully using the correct version of the library.
2. **Analyze the Divergence:** Before fixing the precision bug, run the successfully compiled `./sim` to generate `output.csv`. Compare `output.csv` against `baseline.csv`. Identify the exact iteration number (where the first data row is iteration 1) where the absolute difference in the `value` column first strictly exceeds `0.01`.
3. **Fix the Precision Loss:** Modify `simulate.cpp` to eliminate the precision loss. All floating-point math should be performed with `double` precision.
4. **Verify the Fix:** Recompile and re-run `./sim`. The new `output.csv` must match `baseline.csv` very closely (maximum absolute difference across all rows must be less than `1e-5`).
5. **Generate Diagnostic Log:** Create a file at `/home/user/sim_project/diagnostic.log` with exactly the following format:
```
First divergence iteration: [ITERATION_NUMBER]
Library linked: [EXACT_NAME_OF_THE_SO_FILE_LINKED]
```
*(For example: `Library linked: libmath_v3.so`)*

Do not use root/sudo privileges. Ensure your final `diagnostic.log` and the corrected `simulate.cpp` are left in the `/home/user/sim_project` directory.