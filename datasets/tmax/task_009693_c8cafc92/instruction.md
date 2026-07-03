You are an operations data analyst. Every day, different web servers upload access logs in CSV format, but because they run different server software, the columns in the CSVs are not always in the same order. 

Your task is to build a reproducible, Bash-based ETL pipeline script that normalizes and aggregates these logs.

First, create a Python virtual environment at `/home/user/venv` and install the `csvkit` package inside it to help process the CSV files.

Next, write a Bash script at `/home/user/pipeline.sh` that does the following when executed:
1. Sources the virtual environment.
2. Creates the directories `/home/user/processed` and `/home/user/reports` if they do not exist.
3. Reads all CSV files from `/home/user/raw/` (e.g., `server1.csv`, `server2.csv`, `server3.csv`).
4. Extracts exactly four columns from each file in this exact order: `IP`, `Date`, `Endpoint`, `Status`.
5. Filters out any rows where the `Status` code is 500 or greater (we only want successful or client-error requests).
6. Concatenates the filtered data into a single file at `/home/user/processed/master_log.csv`. The final file must have exactly one header row (`IP,Date,Endpoint,Status`).
7. Computes the total number of requests per `Endpoint` from the `master_log.csv` and generates a Markdown report at `/home/user/reports/summary.md`.

The `/home/user/reports/summary.md` must have the following exact format, sorted alphabetically by Endpoint:
```markdown
# Endpoint Summary
- /api/auth: [COUNT]
- /api/data: [COUNT]
- /api/users: [COUNT]
```

Note: 
- The raw files are already placed in `/home/user/raw/`.
- Make sure your script handles the header row properly when concatenating so that `master_log.csv` has only one header row at the very top.
- The `pipeline.sh` script must be fully self-contained, reproducible, and executable. Run it to generate the final processed files.