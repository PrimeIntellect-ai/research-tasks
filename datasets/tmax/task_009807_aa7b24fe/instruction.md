You are a researcher running a simulation of molecular network signal propagation. You have a Rust project located in `/home/user/sim_project`. The program is intended to compute a random walk on a molecular graph defined in `/home/user/molecule.txt` and record the signal intensity at node 0 over 100 time steps. 

Currently, the code suffers from a severe numerical stability issue: the transition matrix is incorrectly calculated as `adj[i][j] * 1.5` instead of the proper random walk transition probability, causing the state values to explode to infinity.

Your tasks are:
1. Identify and fix the numerical instability in `/home/user/sim_project/src/main.rs`. Modify the code so that the transition matrix `trans[i][j]` correctly represents the probability of moving from node `i` to node `j` (i.e., `adj[i][j] / deg[i]`).
2. Build and run the fixed Rust project. It will generate a file `/home/user/sim_project/signal.txt` containing 100 lines of signal values.
3. Write a bash regression test script at `/home/user/run_regression.sh`. The script must:
   - Compile and execute the Rust code in `/home/user/sim_project`.
   - Read the 100th (final) line of `/home/user/sim_project/signal.txt`.
   - Check if this final signal value is numerically between `0.1` and `0.5` (which indicates a stable, converged distribution).
   - If the value is within the valid range, write `PASS` to `/home/user/regression_result.txt` and exit with code `0`.
   - If the value is outside the range, write `FAIL` to `/home/user/regression_result.txt` and exit with code `1`.

Ensure your bash script is executable.