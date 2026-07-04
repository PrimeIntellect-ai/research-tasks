You are a data engineer tasked with building a lightweight, Bash-native ETL (Extract, Transform, Load) pipeline for server telemetry data. Due to strict environment constraints, you cannot use Python, R, or external databases for the data processing—you must write a Bash script (`/home/user/run_etl.sh`) that uses standard Unix tools (like `awk`, `sed`, `grep`, `bc`) to perform mathematical and data science operations.

The raw data is located at `/home/user/data/telemetry.csv` and contains the following comma-separated columns (with a header row):
`timestamp,server_id,cpu_usage,ram_usage,status,log_message`

Your script `/home/user/run_etl.sh` must execute the following ETL phases and write the results to the `/home/user/output/` directory (create it if it doesn't exist).

**Phase 1: Data Cleaning (Missing Values & Outliers)**
Read `telemetry.csv` and filter the records:
1. Remove the header row from the output.
2. Remove any row where `cpu_usage` or `ram_usage` is empty.
3. Remove any row where `cpu_usage` is an outlier, defined strictly as `cpu_usage < 0` or `cpu_usage > 100`.
Save the cleaned, header-less data to `/home/user/output/cleaned.csv`.

**Phase 2: Correlation Analysis**
Using the cleaned data from Phase 1, calculate the Pearson correlation coefficient between `cpu_usage` (X) and `ram_usage` (Y). 
Write the final correlation coefficient, rounded to exactly 3 decimal places, to `/home/user/output/correlation.txt`.

**Phase 3: Bayesian Inference**
Calculate the empirical posterior probability that a server will crash given its CPU usage is strictly greater than 85.0. 
Formula: P(status="CRASH" | cpu_usage > 85.0) = Count(status="CRASH" AND cpu_usage > 85.0) / Count(cpu_usage > 85.0).
Assume there is at least one record with CPU > 85.0 in the cleaned data.
Write the probability, rounded to exactly 3 decimal places, to `/home/user/output/bayes.txt`.

**Phase 4: Text Retrieval / "Embedding" Match**
For all rows in the cleaned data where `status` is "CRASH", find the `log_message` that is most similar to the target query: "database connection timeout".
To determine similarity without an embedding model, implement a simple Jaccard index over words (case-insensitive). 
- Tokenize both the query and the log messages into sets of alphabetic-only words (convert to lowercase, strip punctuation).
- Jaccard Index = (Intersection of word sets) / (Union of word sets).
If there is a tie, pick the log message that appears first chronologically (lowest timestamp).
Write the EXACT original `log_message` (preserving its original casing and punctuation) to `/home/user/output/retrieval.txt`.

Make sure `/home/user/run_etl.sh` is executable and can run completely unattended to produce the exact output files.