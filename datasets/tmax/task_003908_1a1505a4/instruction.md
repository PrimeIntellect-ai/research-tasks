You are a performance engineer analyzing a numerical simulation in a Rust application located at `/home/user/stat_sim`. 

This simulation models a convergence process where a state variable `x` iteratively moves towards a target value of `100`. The simulation is run for a batch of starting values from `-100` to `50`. 

Currently, the profiling shows two critical issues:
1. **Statistical Anomaly**: The final converged values are often completely wrong, leading to bizarre averages.
2. **Convergence Failure / Loop Termination**: The simulation frequently hits the failsafe step limit (`10_000` steps) instead of naturally terminating, which causes terrible performance.

Your tasks are:
1. Investigate the code in `/home/user/stat_sim/src/main.rs`. 
2. Identify and fix the signed integer overflow causing the statistical anomaly.
3. Fix the loop termination and convergence failure: The step size is calculated as `(100 - x) / 2`. When `x` gets very close to `100`, integer division truncation causes the step size to become `0` before `x` reaches `100`. Modify the logic so that if the calculated step size is `0` but `x` is less than `100`, the step size is forced to `1`. This will guarantee convergence.
4. Ensure the failsafe loop limit (`10_000`) remains in the code as a fallback.
5. After fixing the bugs, run the application and redirect its standard output to `/home/user/result.txt`.

The output of the application is a single integer representing the total sum of steps taken across all starting values.