You are a FinOps analyst tasked with optimizing cloud costs and automating the ingestion of daily billing reports. You need to create a Git-based automated pipeline that processes billing data, converts timestamps to the correct local timezone, calculates network egress costs, and securely backs up the raw data before it is committed.

Perform the following tasks:

1. Create a Git repository at `/home/user/finops_pipeline`.
2. Create a backup directory at `/home/user/backups`.
3. Configure a `pre-commit` Git hook in the `finops_pipeline` repository that does the following every time a commit is made:
    * **Backup**: Finds all `.csv` files currently staged for commit, archives them into a compressed tarball, and saves it to `/home/user/backups/raw_backup_latest.tar.gz`.
    * **Process**: Reads the staged `.csv` files. The CSV files have a header and four columns: `Timestamp,Service,Region,Cost`.
    * **Filter & Timezone Conversion**: Filters the data for rows where the `Service` is exactly `EgressNetwork`. The `Timestamp` column is provided in UTC format (e.g., `2023-10-15T03:00:00Z`). You must convert this timestamp to the `America/New_York` timezone to determine the local date (format `YYYY-MM-DD`). 
    * **Aggregate**: Sums up the `Cost` of `EgressNetwork` usage per local `America/New_York` date.
    * **Output**: Writes the aggregated results to a file named `network_daily_costs.log` in the root of the repository. The file must be sorted chronologically by date. Each line must exactly match the format: `YYYY-MM-DD: $<TotalCost>` (e.g., `2023-10-14: $5.50` - ensure the cost is formatted to two decimal places).

4. Finally, to test your pipeline:
    * A raw billing file has been provided at `/home/user/data/input_billing.csv`.
    * Copy this file into your `finops_pipeline` repository.
    * Stage the file and commit it with the message "Add initial billing data".
    * Ensure the `pre-commit` hook successfully runs, creates the backup, and generates the correct `network_daily_costs.log`.

Note: You may use shell commands, `awk`, `sed`, or scripting languages like Python (which is installed) inside your Git hook to accomplish this. Ensure your hook is executable.