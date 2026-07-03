You are an operations engineer triaging an incident for a legacy mathematical microservice. The service evaluates a set of telemetry data using a root-finding algorithm. The service used to work, but after a recent refactoring, the automated build is failing, and the outputs are known to be completely incorrect.

The codebase is located at `/home/user/calc_engine`. 

Here is your triage report:
1. **Build Failure**: The project no longer compiles. You need to identify the compiler/linker errors when running `make` and fix the `Makefile`.
2. **Missing Secret Coefficient**: A critical constant (`MAGIC_COEFF`) was accidentally redacted in `config.h` in the latest commit. The correct value is buried somewhere in the Git history of the repository. You must find it and restore it in `config.h`.
3. **Corrupted Input Handling**: The telemetry file `/home/user/calc_engine/data.txt` has developed corrupted entries (e.g., `ERR`, `NaN`, or random strings). The current `main` loop stops parsing entirely when it hits the first bad line, ignoring the rest of the file. You must modify `solver.c` to gracefully skip non-numeric tokens and continue summing the results for all valid numeric lines.
4. **Convergence Failure**: Even when the input parses, the Newton-Raphson root-finding method in `solver.c` produces incorrect, artificially low results for certain inputs. You must repair the convergence logic (hint: look at the termination condition and consider the absolute error).

Your goal is to successfully compile the code, process all valid data points in `data.txt`, and output the correct sum of the roots. 

Once you have fixed the code, run `./solver` and save the exact console output (which should print `Total Sum: <value>`) to `/home/user/results.log`. 

Ensure `/home/user/results.log` is created. Do not change the overall logic of the math equation, only fix the bugs described.