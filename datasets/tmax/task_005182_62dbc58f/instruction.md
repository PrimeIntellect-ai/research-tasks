You are a performance engineer tasked with profiling a mesh simulation tool to analyze its parallel scaling behavior. 

We have a mesh simulator located at `/home/user/sim.py`. It simulates a domain decomposition task and reads the environment variable `OMP_NUM_THREADS` to determine the number of threads. It outputs a single floating-point number representing the execution time in seconds.

Your task is to write a Bash script at `/home/user/profile.sh` that orchestrates this profiling, validates it against an analytical strong-scaling model, and calculates the deviation.

The script must perform the following:
1. Loop through the thread counts: 1, 2, 4, and 8.
2. For each thread count, set the `OMP_NUM_THREADS` environment variable and run the simulator for a mesh size of 1024 (`python3 /home/user/sim.py --mesh 1024`).
3. Record the Actual Time.
4. Calculate the Analytical Ideal Time for each thread count, which assumes perfect strong scaling. The ideal time is calculated as: `IdealTime = ActualTime_for_1_thread / current_threads`.
5. Calculate the Scaling Efficiency: `Efficiency = IdealTime / ActualTime`.
6. Output these metrics to `/home/user/results.csv`. The file must have the exact header: `Threads,ActualTime,IdealTime,Efficiency`. All float values must be formatted to exactly 4 decimal places.
7. Perform a regression validation: calculate the Mean Squared Error (MSE) between the ActualTime and IdealTime across all 4 runs. Output this single MSE value (formatted to 4 decimal places) to `/home/user/mse.txt`.

Ensure your bash script is executable and run it to generate the final output files. You may use standard Unix tools (like `awk`, `bc`, etc.) within your Bash script to perform the calculations.