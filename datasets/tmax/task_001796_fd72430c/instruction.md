You are assisting a computational physics researcher in validating a fast C-based simulation against an existing legacy simulator. 

We have a legacy simulator provided as a stripped binary at `/app/oracle_sim`. This oracle simulates a non-linear damped harmonic oscillator, but it outputs data in a verbose, messy text format. We need to implement a faster, clean version in C and orchestrate the workflow.

The physical system is governed by the differential equation:
d²x/dt² + γ(dx/dt) + ω²x + αx³ = 0

Parameters for our study:
- ω (omega) = 1.5
- γ (gamma) = 0.2
- α (alpha) = 0.1
Initial conditions:
- x(0) = 2.0
- v(0) = dx/dt(0) = 0.0
- Time span: t = 0.0 to t = 20.0 inclusive
- Time step: dt = 0.01

Your tasks:
1. **Data Reshaping**: Run `/app/oracle_sim` (it takes no arguments and uses the hardcoded parameters above). It will print verbose lines. Parse this output to extract just the `t` and `x` values into a clean CSV format (e.g., using awk, sed, or python).
2. **C Implementation**: Write a C program `/home/user/fast_sim.c` that numerically integrates the above equation using the standard 4th-order Runge-Kutta (RK4) method.
3. **Validation**: Your C program must output its trajectory to `/home/user/sim_results.csv` with exactly three columns: `t,x,v` (comma-separated, with a header row `t,x,v`). Ensure you output values at every `dt = 0.01` step from `0.0` to `20.0`.
4. **Orchestration**: Create a bash script `/home/user/workflow.sh` that:
   - Runs the oracle and parses its output into `oracle_clean.csv` (columns: `t,x`).
   - Compiles `fast_sim.c` into `fast_sim` with `-O2 -lm`.
   - Runs `./fast_sim`.
   - Validates the analytical/numerical match by printing the maximum absolute difference in `x` between `oracle_clean.csv` and `sim_results.csv` to the terminal.

The automated test will evaluate the accuracy of your `/home/user/sim_results.csv` using a quantitative metric threshold. Ensure your numerical precision is high (use `double` for all calculations) and your RK4 implementation is mathematically correct.