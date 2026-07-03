You are an operations engineer triaging a critical incident. Our network path optimizer, written in C, is failing in production. We have isolated the issue to a specific module, but it currently fails to build, crashes when forced to run, and produces incorrect calculations based on the required business logic.

Your workspace is located at `/home/user/incident_1029`.

Here are your objectives:

1. **Dependency Resolution**: 
   The `Makefile` is failing to link the program because it cannot find `libcustommath.so`. This library is pre-compiled and located in `/home/user/incident_1029/lib`. Modify the `Makefile` so that the compiler correctly finds and links this library, and ensure that the runtime linker can also locate it (e.g., using rpath).

2. **Crash Debugging (Recursion Fix)**: 
   Once built, running `./route_optimizer 5 10` causes a Segmentation Fault. Use a debugger to inspect the program. The crash is caused by infinite recursion in `cost_calc.c`. Fix the recursive call so that the depth correctly approaches the base case.

3. **Formula Correction**: 
   The implementation in `cost_calc.c` has mathematical errors. The correct formula for computing the path cost is:
   - **Base case**: When `depth` is 0, the cost is exactly `node * 1.5`. (Note: You must use the provided `custom_multiply` function from the custommath library for this multiplication).
   - **Recursive step**: For a given `node` and `depth > 0`, the next node in the path is calculated as `(node * 3) % 17`. The cost for the current step is the cost of the next node at `depth - 1` divided by `2.0`, plus the current `node` value.

4. **Verification**: 
   After fixing the code and ensuring `make` succeeds without errors, run the program with a starting node of 5 and a depth of 10.
   Save the standard output of this run to `/home/user/incident_1029/solution.txt`. 
   The output should strictly be a single floating-point number printed to 4 decimal places.

Do not change the command-line arguments parsing in `main.c`. Focus only on `Makefile` and `cost_calc.c`.