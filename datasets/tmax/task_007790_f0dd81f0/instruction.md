You are acting as a performance engineer responsible for analyzing a system metrics pipeline. The pipeline currently fails to build, process data, and compute correct statistics. You need to debug and fix the pipeline to generate the correct performance report.

The pipeline is located in `/home/user/profiler/`.

Here are the issues you must resolve:
1. **Dependency Conflict**: The `requirements.txt` file contains a dependency conflict preventing installation. Fix the conflict so that all packages can be installed using `pip install -r requirements.txt`. You may upgrade or downgrade versions to the nearest compatible ones.
2. **Database Recovery**: The SQLite database `/home/user/profiler/metrics.db` is corrupted, but its Write-Ahead Log (WAL) `/home/user/profiler/metrics.db-wal` is intact. Recover the data into a new, uncorrupted database named `/home/user/profiler/recovered.db`.
3. **Formula Implementation Correction**: The script `/home/user/profiler/process_metrics.py` calculates the Exponential Moving Average (EMA) of the CPU usage, but the smoothing factor (alpha) calculation is incorrect, leading to wildly wrong outputs. Find the formula for EMA alpha (given a span) and fix the python script. (Hint: The standard formula for EMA alpha is `2 / (span + 1)`).
4. **Execution**: Run the fixed script using the recovered database to generate the final output:
   `python /home/user/profiler/process_metrics.py --db /home/user/profiler/recovered.db --out /home/user/profiler/output.json`

Your final output must be exactly located at `/home/user/profiler/output.json` and contain the correctly computed moving averages in the format specified by the script.