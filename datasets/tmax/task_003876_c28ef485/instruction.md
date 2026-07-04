You are a data engineer building a lightweight ETL pipeline on a Linux server. You need to process a large events log using only standard Bash tools (shell built-ins, coreutils, awk, sed, etc.) without loading the entire file into memory and without reading the file more than once.

Your input data is located at: `/home/user/data/events.csv`
The CSV has the following header: `id,region,status,amount`
The `status` column contains either `SUCCESS` or `FAILED`.

You must write a Bash script at `/home/user/run_etl.sh` that reads `/home/user/data/events.csv` in a **single streaming pass** (you may only read the input file once). The script must orchestrate a branching pipeline to produce three separate outputs simultaneously in the `/home/user/output/` directory:

1.  `/home/user/output/sample.csv`: A stratified sample containing the CSV header, followed by exactly the *first 3* `SUCCESS` events encountered for *each* `region`. 
2.  `/home/user/output/failed_count.txt`: A single file containing only the total integer count of all `FAILED` events.
3.  `/home/user/output/success_sum.txt`: A single file containing only the total sum of the `amount` column for *all* `SUCCESS` events in the entire file (not just the sampled ones).

Requirements:
- Ensure your script is executable (`chmod +x /home/user/run_etl.sh`).
- Use Bash process substitution or a single `awk` script to achieve the single-pass requirement.
- Do not use Python, Perl, or other non-Bash scripting languages.
- Create the `/home/user/output/` directory if it does not exist.
- Run the script so the outputs are generated.