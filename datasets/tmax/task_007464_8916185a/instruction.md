You are assisting a FinOps analyst who needs to automatically monitor local storage costs and mock an email alert system for expensive directories. 

You must create an idempotent bash deployment script located at `/home/user/deploy_cost_monitor.sh`. The deployment script must perform the following actions:

1. **Environment Configuration:**
   - Idempotently configure the environment variables `FINOPS_RATE=0.15` and `FINOPS_LIMIT=50` inside `/home/user/.bash_profile`.
   - "Idempotent" means if your `deploy_cost_monitor.sh` script is run multiple times, it must not add duplicate lines to `.bash_profile`.
   - Source the `.bash_profile` or export the variables in your script so they are available for the next steps.

2. **Generate Python Analyzer:**
   - The bash script must create a Python script at `/home/user/calculate_costs.py`.
   - The Python script must calculate the total size of all files in the directory `/home/user/project_data/` recursively.
   - Convert the total size into Megabytes (1 Megabyte = 1,048,576 bytes). Keep it as a float.
   - Read the `FINOPS_RATE` and `FINOPS_LIMIT` environment variables. If they are not set, the script must silently default both to `0.0` (which mimics a misconfigured server that silently rejects logging).
   - Calculate the total cost by multiplying the size in MB by `FINOPS_RATE`.
   - If the total cost is strictly greater than `FINOPS_LIMIT`, the script must append exactly the following formatted string to `/home/user/finops_alerts.log` (with cost and limit formatted to exactly two decimal places):
     `[ALERT] Cost exceeds limit: $<cost> (> $<limit>) - Notifying admin@local`
     *(Example: `[ALERT] Cost exceeds limit: $60.00 (> $50.00) - Notifying admin@local`)*

3. **Execution:**
   - Finally, the bash script must execute the generated Python script using `python3 /home/user/calculate_costs.py`.

Ensure your bash script has executable permissions (`chmod +x`). Do not manually create the data directory; assume `/home/user/project_data/` already exists and contains the files to be measured.