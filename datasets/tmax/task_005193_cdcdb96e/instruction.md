You are a performance engineer tasked with debugging a numerical simulation running in an isolated environment. Recently, a background container running our physical simulation started failing. 

You need to investigate the environment located in `/home/user/app/`.

Here is what you know:
1. The container's last run output was dumped to `/home/user/app/logs/crash.log`. Inspect this log to understand the failure.
2. The simulation code is in `/home/user/app/src/sim.c`. It depends on a utility header `calc_utils.h`.
3. There is a dependency conflict: the build script (`/home/user/app/build.sh`) is accidentally pulling in an outdated version of the utility headers from the `deps/v1` directory instead of the correct `deps/v2` directory. This is causing a convergence failure in the simulation's iterative loop because of an incorrectly defined `UPDATE_RATE` macro.
4. Your first goal is to create a Minimal Reproducible Example (MRE). Create a file named `/home/user/app/mre.c` that:
   - Includes `<stdio.h>` and `<calc_utils.h>`
   - Has a `main` function.
   - Initializes a `double` variable `x = 10.0;`.
   - Simulates 10 iterations of the core loop by applying `x = x - UPDATE_RATE * x;` exactly 10 times.
   - Prints the final value of `x` formatted to 2 decimal places (e.g., `printf("%.2f\n", x);`).
   - Returns 0.
5. Compile and run your MRE using the broken include paths to verify it reproduces the divergence (values growing out of control).
6. Next, fix the dependency conflict. Modify `/home/user/app/build.sh` so that the compiler correctly prioritizes `deps/v2` over `deps/v1`. 
7. Rebuild the main simulation by running the fixed `/home/user/app/build.sh`.
8. Run the newly compiled `/home/user/app/sim`. It should now converge successfully.
9. Create a log file at `/home/user/app/solution.txt`. On the first line, write the final printed output of the fixed `/home/user/app/sim`. On the second line, write the name of the directory (`v1` or `v2`) that contained the faulty `UPDATE_RATE` macro.

Ensure all file paths are exactly as specified and correct permissions are maintained.