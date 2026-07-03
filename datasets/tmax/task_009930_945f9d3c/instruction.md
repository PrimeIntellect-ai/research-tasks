You are a DevOps engineer assisting a quantitative trading team. Their C++ Monte Carlo pricing service, `mc_pricer`, has suddenly started crashing during a specific batch processing job. The service spawns threads to calculate statistics over large datasets, but the latest run on `/home/user/mc_pricer/data.csv` is failing. Logs indicate that a crucial thread is being killed due to a failed assertion related to `NaN` (Not a Number) values, leading to a core dump or immediate exit.

Your task is to perform forensic analysis and environment repair to get this service back up and running.

Here is your workflow:
1. **Environment & Build Repair**: Navigate to `/home/user/mc_pricer`. You will find the source code and a `Makefile`. The current build environment is misconfigured. The `Makefile` is failing to link the threading library correctly and lacks debug symbols. Fix the `Makefile` so the project builds successfully and produces a debug-friendly executable named `mc_pricer`.
2. **Forensic Diagnosis**: Run the compiled binary. It will crash. Use a debugger (`gdb`) or other forensic techniques to identify the exact cause of the crash. The issue is rooted in a numerical instability occurring under specific data conditions.
3. **Write the Diagnosis Report**: Create a file at `/home/user/diagnosis.txt` strictly following this format (replace placeholders with your findings):
   ```
   BUGGY_FILE: <name of the C++ file where the bug occurs>
   BUGGY_LINE: <the exact line number where the mathematically invalid operation produces NaN>
   NaN_VARIABLE: <the name of the local variable that first becomes NaN on that line>
   ```
4. **Code Fix**: Modify the C++ code to fix the numerical instability. The current algorithm for calculating variance is susceptible to catastrophic cancellation when processing data with a massive mean and tiny variance. Implement a numerically stable algorithm (e.g., Welford's online algorithm or a stable two-pass algorithm) to correctly compute the variance and standard deviation without resulting in negative variance or `NaN`.
5. **Generate Final Output**: Recompile and run the fixed `mc_pricer` binary. It will process `data.csv` and output a single floating-point number (the calculated standard deviation) to standard output. Save this exact output to `/home/user/result.txt`.

Ensure all operations are done within `/home/user/mc_pricer`. Do not change the overall architecture or output format of the program; only fix the mathematical instability.