You are a performance engineer tasked with debugging a Bash-based mathematical analysis tool. 

In `/home/user/math_proj`, there is a project that calculates the maximum Collatz conjecture sequence length for numbers up to 500. You need to get the script running, and then optimize it so it completes in under 2 seconds.

Currently, the project suffers from several issues:
1. **Build/Dependency Failure**: If you try to run `./run_analysis.sh`, it fails. The logs in `/home/user/math_proj/logs/build.log` contain the traceback of a previous run. There is a conflict/error stemming from how the script sources its mathematical dependencies from the `lib/` directory. Fix the dependency inclusion in `run_analysis.sh` so it only uses the correct, working library version.
2. **Performance Bottleneck**: Once the script runs, it is excruciatingly slow. You must diagnose the performance issue in the math library and rewrite the mathematical operations inside the `collatz` function to be highly efficient using only native Bash built-ins. Do not change the algorithmic logic (it must remain a standard while-loop), but replace the slow external command calls with fast Bash arithmetic.

Your goal:
1. Fix the dependency sourcing bug in `/home/user/math_proj/run_analysis.sh`.
2. Optimize the `collatz` function in the correctly sourced library so the script runs extremely fast.
3. Run `./run_analysis.sh`. It will automatically output a file at `/home/user/math_proj/result.txt`.

The final output in `/home/user/math_proj/result.txt` must strictly follow the format produced by the script (e.g., `Max Length: X, Number: Y`).