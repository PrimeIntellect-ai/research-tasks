You are an AI assistant helping a data scientist automate a dataset cleaning and reporting pipeline using shell utilities. 

Your task is to create a fully automated ETL pipeline using only bash, standard coreutils (awk, sed, grep, etc.), and `sqlite3`.

Here is the setup:
- A simulated remote directory exists at `/home/user/remote_staging/` containing a messy dataset named `raw_data.csv`.
- A template file exists at `/home/user/templates/report.tmpl`.

You need to write a master bash script at `/home/user/pipeline.sh` that performs the following steps when executed:

1. **Local-Remote Transfer Simulation**:
   Copy `/home/user/remote_staging/raw_data.csv` to `/home/user/local_processing/working_data.csv`.

2. **Data Cleaning (String/Text Processing)**:
   Process `working_data.csv` (which has a header `ID,Name,Email,Score,Department`) into a cleaned CSV file at `/home/user/local_processing/cleaned_data.csv`.
   Cleaning rules:
   - Remove any leading/trailing spaces from all fields.
   - Convert all `Email` addresses to strictly lowercase.
   - Remove any rows where the `Score` column is completely empty.
   - Keep the CSV header in the cleaned file.

3. **Database Bulk Import**:
   Create an SQLite database at `/home/user/db/analytics.sqlite`.
   Create a table named `employee_stats` with the schema:
   `CREATE TABLE employee_stats (id INTEGER, name TEXT, email TEXT, score INTEGER, department TEXT);`
   Bulk import the `cleaned_data.csv` into this table (skip the header row during import).

4. **Template-Based Text Generation**:
   Query the SQLite database to calculate the average score per department, formatted as `Department: <Average Score>` (round the average to 1 decimal place or just use exact integer if they divide evenly). Sort alphabetically by department.
   Query the total number of valid records in the database.
   Read the template file `/home/user/templates/report.tmpl` which contains placeholders `__TOTAL_RECORDS__` and `__DEPT_STATS__`.
   Replace `__TOTAL_RECORDS__` with the total row count.
   Replace `__DEPT_STATS__` with the multi-line department averages text.
   Save the final text to `/home/user/reports/final_report.md`.

5. **Pipeline Scheduling**:
   Create a cron job configuration file at `/home/user/cron.conf` that schedules `/home/user/pipeline.sh` to run every day exactly at 3:30 AM.

Ensure that `/home/user/pipeline.sh` is executable and run it once to generate the database and report.

Note: You will need to create the directories `/home/user/local_processing`, `/home/user/db`, and `/home/user/reports` inside your script or before running it.