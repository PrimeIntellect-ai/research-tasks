You are acting as a FinOps analyst responsible for optimizing and tracking cloud infrastructure costs. 

We have a daily cost aggregation script located at `/home/user/cost-analyzer.sh`. It queries our internal tool `cloud-cost-cli` to fetch the previous day's resource costs, calculates the total sum, and saves the report. This script is executed by a scheduled CI/CD pipeline job.

However, the pipeline job runs in a highly restricted, clean environment (similar to standard cron). Because of this, the script is currently silently failing to find the CLI tool and is writing an empty total to the report file (`Total Cost: $`). 

Your task is to fix and improve `/home/user/cost-analyzer.sh` with the following requirements:
1. **Fix the Path Issue:** The `cloud-cost-cli` executable is located in `/home/user/bin/`. You must modify the script so it can successfully execute this tool even when run in an empty environment (`env -i`).
2. **Add Robust Error Handling:** The script currently fails silently if the CLI tool is missing or fails. Modify the script so that if `cloud-cost-cli` cannot be found or returns a non-zero exit code, the script immediately aborts and exits with code `1`. Do not write to the report file if the data extraction fails.
3. **Data Processing:** The script must take the CSV output from `cloud-cost-cli` (which has a header `service,cost`) and sum the values in the `cost` column. 
4. **Final Output:** The script must write the result to `/home/user/reports/daily_cost.log` exactly in this format: `Total Cost: $<SUM>` (e.g., `Total Cost: $150.25`). Create the `/home/user/reports` directory if it does not exist.

Ensure your updated script relies only on standard bash features and coreutils (like `awk`, `grep`, etc.).