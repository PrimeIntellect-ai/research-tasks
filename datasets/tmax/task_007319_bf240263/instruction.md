You are a performance engineer tasked with debugging a batch mathematical processing system. 

The system evaluates complex polynomials using a pre-compiled binary `/home/user/project/bin/poly_eval`. This binary is executed across multiple input files using a shell script located at `/home/user/project/run_batch.sh`.

Currently, the system is failing in three ways:
1. The shell script crashes or skips certain input files in `/home/user/project/data/`. You will need to debug and fix `run_batch.sh`.
2. Even when the script is fixed, the mathematical outputs are wildly incorrect. We suspect `poly_eval` is dynamically linking to an outdated system library (`/home/user/syslib/libmathops.so`) instead of the correct project-specific library (`/home/user/project/lib/libmathops.so`). 
3. We need to strictly validate the underlying math operations.

Your tasks:
1. Fix `/home/user/project/run_batch.sh` so it correctly processes all files in the `data` directory, including those with spaces in their filenames.
2. Reverse engineer `poly_eval` to identify the exact function signature it imports from `libmathops.so`. 
3. Resolve the dependency conflict so that `poly_eval` uses the library in `/home/user/project/lib/`.
4. Write a C program at `/home/user/project/verify.c` that dynamically loads the correct `libmathops.so` (using `dlopen`), calls the identified mathematical function using the inputs `5.0` and `3.0`, and uses `assert()` to validate that the result is strictly greater than 0. 
5. Run your fixed `run_batch.sh` and redirect all its standard output to `/home/user/project/results.log`.

The final state must have:
- A successfully compiling and passing `/home/user/project/verify.c`.
- A log file at `/home/user/project/results.log` containing the correct output from the batch script. Format of each line should be: `[filename]: [result]` exactly as output by the correctly linked binary.