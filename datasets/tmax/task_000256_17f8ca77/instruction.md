You are a DevOps engineer debugging a statistical anomaly in a data ingestion pipeline.

Our network metrics pipeline uses a Bash script located at `/home/user/calculate_metrics.sh` to process network packet logs from `/home/user/traffic_logs.csv`. The script calculates a "Weighted Traffic Score" by multiplying the `bytes` of each packet by a scaling factor of `10000000000000000` (10^16) and summing them up. 

Recently, the monitoring dashboard started showing negative values for this metric, triggering a statistical anomaly alert. Your investigation reveals that the system recently migrated to a new container environment.

Your tasks:
1. Diagnose the root cause of the negative metric value. (Hint: inspect how Bash handles the arithmetic operations in the script).
2. Fix `/home/user/calculate_metrics.sh` so that it accurately computes the total sum of the weighted scores without suffering from numerical instability or wraparound. You may use standard tools available in the Linux environment (like `awk`, `bc`, or `python`) to bypass Bash's native arithmetic limits, but the main wrapper must remain a Bash script.
3. Run the fixed script and save the precise, correct final numerical output (just the number) to `/home/user/final_metric.txt`.

Ensure the script can process the entire `/home/user/traffic_logs.csv` file without errors and outputs the exact positive integer string.