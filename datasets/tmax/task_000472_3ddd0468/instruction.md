You have recently inherited an unfamiliar codebase for a distributed physics simulation data processor located in `/home/user/sim_project`. The system processes numerous input data files in parallel, computing statistical weights and aggregating the results. 

However, the pipeline is currently failing. When you run `python main.py`, it eventually crashes with an environment error, and the log files are scattered and chaotic.

Your objectives are:
1. **System Call & State Tracing:** Identify why the system is crashing. The previous maintainer mentioned something about "running out of resources," but the logs are heavily obfuscated. Use system call tracing tools (like `strace`) and trace the intermediate states to figure out the root cause of the resource exhaustion and fix the resource leak in `main.py`.
2. **Numerical Instability Diagnosis:** The resource exhaustion is actually a secondary effect of an underlying mathematical bug. A specific input causes a numerical instability (overflow) in `utils.py`. Identify the mathematical operation causing this, and implement a numerically stable equivalent (e.g., the max-shift trick for exponentials).
3. **Log Timeline Reconstruction:** Look at the logs generated in `/home/user/sim_project/logs/` to identify the exact input file that initially triggers the numerical instability. Write the name of this file into `/home/user/sim_project/bad_file.txt`.
4. **Regression Test Construction:** Create a regression test file at `/home/user/sim_project/test_regression.py`. It must import the fixed mathematical function from `utils.py` and contain a function `test_stability()` that proves the function no longer crashes when given extremely large input values (e.g., `[1000.0, 1000.0, 1000.0]`).
5. **Successful Execution:** Run `python main.py` successfully to completion. It should generate a final output file `/home/user/sim_project/aggregate_result.txt`.

Ensure all code changes are made in place, the regression test passes, and the final `aggregate_result.txt` is successfully generated.