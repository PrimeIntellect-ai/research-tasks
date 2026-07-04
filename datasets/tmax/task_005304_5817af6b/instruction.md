You are tasked with debugging a failing build for a C++ physics simulation tool. The project is located in `/home/user/project`. 

Currently, when you source the environment script and run `make`, the build fails or the execution produces incorrect results. 

Your goals are to debug and fix the pipeline so that the final executable builds successfully and computes the correct simulation output.

Specifically, you need to:
1. **Fix the Environment**: The build relies on `env.sh` to set up paths. There is a misconfiguration preventing the compiler from finding the standard math library paths or causing linkage errors. Diagnose and repair `env.sh`.
2. **System Call Tracing**: The pre-computation tool `calc_weights` is failing to read an input file because it looks for a dynamically determined configuration file path. Use system call tracing (e.g., `strace`) to figure out what file it is trying to open and ensure that file exists with the content `1e-15`.
3. **Fix Numerical Instability**: The `src/calc_weights.cpp` file contains a function computing `(exp(x) - 1.0) / x`. For the required small input values (like `1e-15`), this calculation suffers from catastrophic cancellation, resulting in `NaN` or `0.0` instead of a value near `1.0`. Modify `src/calc_weights.cpp` to use a numerically stable equivalent (e.g., `expm1(x) / x` or a Taylor expansion for very small `x`).
4. **Run and Verify**: Once the environment is fixed, the missing file is placed correctly, and the C++ numerical bug is resolved, run `make clean && make`. Then, execute `./sim_app` and redirect its standard output to `/home/user/project/final_output.log`.

The `/home/user/project/final_output.log` should contain exactly one line with the correctly computed non-NaN floating-point result.