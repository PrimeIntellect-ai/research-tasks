You are an engineer tasked with investigating a memory leak and a bug in a long-running C++ math simulation service. The service computes trajectories based on time intervals, but it is currently crashing, leaking memory, and failing to build in the current environment.

The codebase is located at `/home/user/sim_daemon/`.

Here is what you need to do:
1. **Fix Environment Misconfiguration**: The `build.sh` script fails. It requires an environment variable `SIM_ENV` to be set to `production` during compilation. Modify `/home/user/sim_daemon/build.sh` to correctly set and export this variable before running `g++`.
2. **Floating-point Precision Repair**: In `/home/user/sim_daemon/sim_server.cpp`, the simulation loop uses a floating-point equality check (`time != target_time`) to determine when to stop. Because of how floating-point numbers are represented, this often creates an infinite loop, filling up memory until a safety limit is hit. Change the loop condition to robustly handle floating-point advancement (e.g., `time < target_time - 1e-9` or similar).
3. **Memory Leak**: The `TrajectoryState` objects are dynamically allocated and pushed to a `std::vector` inside `run_simulation`, but they are never freed before the function returns. Fix the memory leak so that all allocated memory is properly freed.
4. **Assertion-based Validation**: Inside the simulation loop in `run_simulation`, add an assertion: `assert(states.size() <= 1000);` to ensure the vector never exceeds 1000 elements. You will need to `#include <cassert>`.
5. **Regression Test Construction**: Create a regression test script at `/home/user/test.sh` that does the following:
   - Compiles the code by running `/home/user/sim_daemon/build.sh`.
   - Runs the compiled binary `./sim_server` under `valgrind --leak-check=full`.
   - The binary expects an input file. Provide it an input file `/home/user/test_input.txt` containing the single number `1.0`.
   - Redirect valgrind output to `/home/user/valgrind_out.txt`.
   - Exit with code 0 if valgrind reports "0 bytes in 0 blocks" definitely lost, otherwise exit with code 1.

Ensure your code compiles and the test script correctly identifies that the leak is gone.