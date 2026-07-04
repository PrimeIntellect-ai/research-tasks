You are an operations engineer triaging an incident involving a critical numerical optimization service written in C. The service has been experiencing sudden convergence failures and crashes. 

Here is what we know:
1. The service evaluates the roots of a specific polynomial using the Newton-Raphson method. 
2. Recently, the frontend started sending inputs with unpredictable whitespace (e.g., `"  1.5  "` instead of `"1.5"`). This seems to trigger a bug in the C solver's input parsing, leading to uninitialized values being fed into the math routines, which then fail to converge or crash completely.
3. We have a memory dump from the latest crash located at `/app/core.dump`. You should analyze it to extract the exact `CRASH_INPUT` string that triggered the fatal error.
4. The original developer left behind an image of their whiteboard notes at `/app/whiteboard.png`. This image contains the required convergence parameters (`MAX_ITER` and `TOLERANCE`) that the algorithm *must* use to match our new precision standards. The current C code is using outdated, hardcoded parameters.
5. Multiple services log to `/app/logs/`. You can cross-reference the timestamps to see how the malformed input propagates, but your primary goal is fixing the solver code.

Your tasks:
1. Extract the correct `MAX_ITER` and `TOLERANCE` values from `/app/whiteboard.png`.
2. Extract the `CRASH_INPUT` string from `/app/core.dump` to understand the input structure.
3. Inspect and fix the source code at `/home/user/solver.c`. Fix the string parsing logic so it robustly handles leading/trailing spaces and multiple spaces without crashing or reading garbage data. 
4. Update the convergence parameters in the C code using the values you found in the whiteboard image.
5. Compile your fixed code to an executable named `/home/user/solver_fixed`.

Your compiled executable `/home/user/solver_fixed` must take a single command-line argument (the input string, potentially containing arbitrary spaces) and print only the final computed float root with 6 decimal places (e.g., `1.234567`), or `CONVERGENCE_FAILURE` if it exceeds the maximum iterations. 

An oracle binary is provided at `/app/oracle_solver`. Your executable must perfectly match the output of this oracle for any input string.