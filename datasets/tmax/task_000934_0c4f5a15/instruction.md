You are an automation specialist tasked with building a text processing workflow. We receive a daily batch of raw system messages, and we need an automated ETL pipeline to parse, group, and load these messages into a database.

Here are your requirements:

1. **Input Data:**
   There is a raw log file located at `/home/user/raw_logs.txt`. 
   Each line in this file follows the format: `timestamp|user_id|message`

2. **Text Processing (Python):**
   Create a Python script at `/home/user/process.py` that reads `/home/user/raw_logs.txt`.
   For each message:
   - Extract the `message` portion.
   - Tokenize the message into words by splitting on whitespace.
   - Clean each word by stripping all non-alphanumeric characters from both ends, and convert it to lowercase. Ignore empty strings.
   - Calculate the frequency of each cleaned word per `user_id`.
   - Output the results to a CSV file at `/home/user/processed.csv` (without a header line). The columns must be: `user_id,word,frequency`.
   - The CSV must be sorted primarily by `user_id` (alphabetically, ascending), secondarily by `frequency` (descending), and tertiarily by `word` (alphabetically, ascending).

3. **Database Bulk Import (Bash/SQLite):**
   Create an executable Bash script at `/home/user/etl.sh` that:
   - Executes `/home/user/process.py`.
   - Creates a new SQLite database at `/home/user/stats.db` (removing it first if it already exists).
   - Creates a table named `word_stats` with columns `user_id TEXT`, `word TEXT`, and `frequency INTEGER`.
   - Uses SQLite's bulk import feature to load `/home/user/processed.csv` directly into the `word_stats` table.

4. **Pipeline Scheduling (Cron):**
   Schedule `/home/user/etl.sh` to run automatically every Monday at 3:15 AM using the user's crontab.

Make sure your scripts are robust. Ensure `/home/user/etl.sh` has the correct execute permissions.