You are acting as a support engineer tasked with collecting diagnostics for a mathematical simulation engine that has started producing incorrect results. The simulation works on smaller datasets but generates mathematical anomalies on specific client inputs due to a suspected signed integer overflow. 

Your objective is to trace the execution, identify the failing input, build a regression test, add assertion-based validation, and correct the bug.

Here is your environment and starting state:
- Workspace: `/home/user/sim_project`
- The simulation binary is compiled via `make` and executed via `/home/user/sim_project/run_sim.sh`.

Please perform the following steps:

1. **System Call Tracing**: The script `run_sim.sh` runs the simulation engine, which reads configuration from a dynamically generated, hidden temporary file in `/tmp/`. Run the script and use system call tracing (`strace`) to discover the exact absolute path of the configuration file opened by the `sim_engine` binary. Read this file to find the two integer parameters: `initial_pos` and `velocity_factor`.

2. **Assertion-Based Validation**: The math logic is inside `/home/user/sim_project/trajectory.c` in the function `int calc_step(int current, int velocity)`. The function computes `(current * velocity) % 1000003`. 
   Modify `trajectory.c` to include an `#include <assert.h>` and add an `assert()` statement right before the calculation that ensures the multiplication of `current` and `velocity` will NOT exceed the maximum value of a 32-bit signed integer (`INT_MAX` from `<limits.h>`). 

3. **Regression Test Construction**: Create a standalone C file at `/home/user/sim_project/test_regression.c`. This program must:
   - Include `trajectory.h`
   - Call `calc_step(initial_pos, velocity_factor)` using the exact values you found in step 1.
   - Return 0 if successful.
   Compile this test file alongside `trajectory.c` to an executable named `test_runner`. When run with your new assertions, this test should intentionally abort due to the assertion failure (proving you caught the overflow).

4. **Bug Fix & Reporting**: 
   - Fix the bug in `trajectory.c` by casting the intermediate multiplication to a 64-bit integer (`long long`) before applying the modulo, preventing the overflow. Remove or adjust the assertion so it no longer fails.
   - Recompile and run `./test_runner`. 
   - Capture the newly corrected output of `calc_step` for those client parameters.
   - Create a diagnostic log at `/home/user/diagnostic_report.txt` with the following strict format:

```
FAILING_FILE: <absolute_path_to_the_tmp_file_found_via_strace>
PARAM_INITIAL_POS: <value>
PARAM_VELOCITY: <value>
CORRECTED_RESULT: <the_correct_modulo_result>
```