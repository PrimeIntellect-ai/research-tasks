You are a performance engineer tasked with debugging a data processing pipeline that has recently started hanging indefinitely, pinning the CPU at 100%. 

The script, located at `/home/user/analyze_metrics.sh`, processes a log file of query results (`/home/user/query_results.log`) and iteratively calculates a steady-state metric using a simple convergence algorithm. However, due to recent changes in the upstream query format, the script now fails to converge and loops forever.

Your objectives:
1. Identify why the script is hanging. (Hint: trace the system calls or bash execution to observe the data parsing and convergence failure).
2. Fix the edge-cases in the format parsing within `/home/user/analyze_metrics.sh` so that it correctly handles all valid data points and properly calculates the differences.
3. Ensure the convergence failure is repaired so the script terminates.
4. Run the fixed script. It is configured to write its final steady-state estimate to `/home/user/final_metric.txt`.

Do not change the mathematical formula or the convergence thresholds in the script. Only fix the data parsing logic so that invalid characters (like commas, trailing metadata, or carriage returns) don't break the calculations and cause the loop to stall.