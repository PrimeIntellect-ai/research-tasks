You are a data engineer tasked with building a lightweight ETL pipeline using only Bash and standard GNU Linux utilities (awk, sed, date, etc.). 

We receive application logs in a messy CSV format. Sometimes, developers log multiline error traces, which results in CSV rows containing embedded newlines inside quoted fields. A naive line-by-line processor silently breaks or drops these rows.

Your task is to build a robust bash-based DAG (Directed Acyclic Graph) to extract, transform, and gap-fill this data.

**Requirements:**

**Phase 1: Extraction & String Parsing (`/home/user/etl/extract.sh`)**
1. Read the input file: `/home/user/data/raw_logs.csv`
2. The CSV has three columns: `Timestamp,Level,Message`.
3. The `Message` field is enclosed in double quotes if it contains commas or newlines.
4. Your script must correctly parse this CSV, replacing any embedded newlines *inside* the quoted messages with the literal string `\n` (a backslash followed by an 'n').
5. Strip the surrounding double quotes from the `Message` field in the output.
6. Write the cleaned, strictly single-line-per-record CSV to `/home/user/data/extracted.csv`. The output format should be `Timestamp,Level,Message` without quotes.

**Phase 2: Transform & Gap-Filling (`/home/user/etl/transform.sh`)**
1. Read `/home/user/data/extracted.csv`.
2. Filter the records to only include those where `Level` is exactly `ERROR`.
3. Aggregate the number of `ERROR` logs per minute. The timestamps are in `YYYY-MM-DD HH:MM:SS` format. You should group by `YYYY-MM-DD HH:MM`.
4. **Gap-Filling:** The output must contain a continuous minute-by-minute time series from the earliest minute present in the *entire* log file (regardless of log level) to the latest minute present in the file. If a minute has no `ERROR` logs, output a count of `0` for that minute.
5. Write the output to `/home/user/data/transformed.csv`. The format must be exactly `YYYY-MM-DD HH:MM,count`, sorted chronologically.

**Phase 3: Pipeline DAG Orchestration (`/home/user/etl/dag.sh`)**
1. Write a master bash script `/home/user/etl/dag.sh` that acts as your orchestrator.
2. It must execute `extract.sh`, and if successful, execute `transform.sh`.
3. If `raw_logs.csv` does not exist, or if any of the child scripts fail (exit with a non-zero status), `dag.sh` must immediately terminate and exit with status code `1`.
4. Ensure all scripts are executable.

**Phase 4: Scheduling**
1. Schedule `/home/user/etl/dag.sh` to run every 5 minutes using `cron`.
2. Save a backup of your crontab configuration to `/home/user/crontab_backup.txt` using the command `crontab -l > /home/user/crontab_backup.txt`.

**Initial Setup:**
The raw data will be placed in `/home/user/data/raw_logs.csv` before you begin. You must create the `etl` directory. All scripts must use bash/standard GNU coreutils (no Python, Perl, Ruby, etc.).