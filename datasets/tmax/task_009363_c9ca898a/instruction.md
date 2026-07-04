You are tasked with fixing and completing a configuration management pipeline. A previous script failed because it processed CSV files line-by-line and silently corrupted data when the `CommitMessage` field contained embedded newlines.

You need to write a Go program (`/home/user/process.go`) and schedule it. 

Here are the requirements:

1. **Input Data**: Read `/home/user/data/config_changes.csv`. It has the following headers: `ChangeID,AuthorEmail,CostImpact,CommitMessage`. Note that `CommitMessage` is quoted and may contain embedded newlines.
2. **Validation & Filtering**: Parse the CSV correctly. Skip the header. Evaluate the `CostImpact` (which is an integer). You must drop any row where `CostImpact` is less than 0 or cannot be parsed as an integer. This is your quality gate.
3. **Data Masking**: For the valid rows, mask the `AuthorEmail` by replacing everything before the `@` symbol with `***` (e.g., `alice.smith@example.com` becomes `***@example.com`).
4. **Mathematical Aggregation**: Calculate the total sum of `CostImpact` for all valid rows.
5. **Template-based Generation**: Use Go's `text/template` package to write a summary report to `/home/user/report.txt`. The report must EXACTLY match this format:
   ```
   Total Valid Changes: <number_of_valid_rows>
   Total Cost Impact: <sum_of_cost_impact>
   Masked Authors:
   - <masked_email_1>
   - <masked_email_2>
   ...
   ```
   (List the masked authors in the exact order they appear in the valid rows of the CSV).
6. **Pipeline Scheduling**: Create a crontab file at `/home/user/cron.txt` that schedules the execution of your Go script (via `cd /home/user && go run process.go`) to run exactly at minute 0 of every hour.

Ensure your Go script runs successfully and produces the correct `/home/user/report.txt`.