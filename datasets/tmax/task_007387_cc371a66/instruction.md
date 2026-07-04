You are acting as a FinOps analyst trying to automate the calculation of wasted cloud spend from scattered billing reports, while ensuring the analysis process is robust, scheduled, and logs are properly managed.

Your system has a Rust project initialized at `/home/user/finops-analyzer` and raw billing CSV files stored in `/home/user/billing_data/`. 

Perform the following tasks:

1. **Write the Rust Analyzer**: 
   Edit `/home/user/finops-analyzer/src/main.rs`. Write a Rust program that reads CSV data from standard input. 
   The CSV format is: `ResourceID,Type,Status,Cost`. 
   The program must parse the data, find all rows where `Status` is exactly `idle` (case-insensitive), sum the `Cost` (which is a floating-point number), and print ONLY the total sum formatted to two decimal places (e.g., `150.25`) to standard output. 
   Build the project in release mode (`cargo build --release`).

2. **Create the Processing Script**:
   Write a bash script at `/home/user/run_analysis.sh` and make it executable.
   This script must:
   - Use `find` and `cat` (or `awk`) to read all `.csv` files inside `/home/user/billing_data/` (and its subdirectories).
   - Pipe the concatenated data into your compiled Rust binary (`/home/user/finops-analyzer/target/release/finops-analyzer`).
   - Capture the output and append a line to `/home/user/logs/idle_costs.log` in this exact format:
     `[<ISO-8601-TIMESTAMP>] Total idle cost: $<SUM>`
     *(Hint: Use `date -Iseconds` for the timestamp).*

3. **Configure Log Rotation**:
   Create a logrotate configuration file at `/home/user/logrotate.conf`.
   Configure it to manage `/home/user/logs/idle_costs.log` with the following rules:
   - Rotate daily.
   - Keep exactly 7 backups.
   - Compress old log files.
   - Do not throw an error if the log file is missing (`missingok`).

4. **Schedule the Job**:
   Configure the current user's crontab to run `/home/user/run_analysis.sh` at minute 0 of every hour.

Make sure the `logs` directory exists.