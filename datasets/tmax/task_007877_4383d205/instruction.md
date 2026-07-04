You are a FinOps analyst tasked with automating the cost reporting for cloud storage used by different teams.

There is a directory structure at `/home/user/cloud_storage` containing subdirectories for different teams (e.g., `engineering`, `marketing`, `sales`). Each subdirectory contains various files representing stored assets.

Your task is to create a Go program and a Bash wrapper script to calculate the storage costs per team and log the execution.

**Step 1: Write the Go program (`/home/user/finops_report.go`)**
Write a Go script that:
1. Reads the `COST_PER_MB` environment variable (which will contain a float value representing dollars per megabyte, where 1 MB = 1,048,576 bytes).
2. Iterates through the directories in `/home/user/cloud_storage/`. Each folder name represents a team.
3. Calculates the total size in bytes of all files within each team's directory (do not recurse into subdirectories, assume flat files).
4. Calculates the cost for each team: `(Total Bytes / 1048576) * COST_PER_MB`.
5. Gets the current time in the `America/New_York` timezone.
6. Writes the results to `/home/user/report.csv`. 
   - The CSV must have a header: `Team,TotalBytes,Cost,Timestamp`
   - Data rows must be sorted alphabetically by Team name.
   - Cost should be formatted to exactly two decimal places (e.g., `0.50`).
   - Timestamp format must be exactly `YYYY-MM-DD HH:MM:SS MST` (e.g., `2023-10-25 14:30:00 EDT`).

**Step 2: Write the Bash wrapper script (`/home/user/run_report.sh`)**
Write an idempotent Bash script that:
1. Sets the `TZ` environment variable to `America/New_York`.
2. Sets the `COST_PER_MB` environment variable to `0.05`.
3. Ensures the directory `/home/user/logs` exists (creating it if it does not).
4. Compiles the Go program into an executable named `/home/user/finops_report`.
5. Executes the compiled Go program.
6. Appends a line with the text `REPORT_GENERATED_SUCCESSFULLY` to `/home/user/logs/run.log` only if the Go program exits with a status code of 0.

Ensure the Bash script is executable (`chmod +x`). Once created, execute `/home/user/run_report.sh` to generate the report.