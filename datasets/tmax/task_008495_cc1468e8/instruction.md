You are a data analyst tasked with building an automated text processing pipeline. Every day, wide-format regional text reports arrive in a directory. Your job is to create a robust system that reshapes this data into a long format, tokenizes the text, normalizes it, and processes multiple files in parallel.

You must build this pipeline according to the following specifications:

1. **The Data:**
   You will find 3 pipe-delimited data files in `/home/user/incoming/` (e.g., `day1.dat`, `day2.dat`, `day3.dat`). 
   Each file has no header. Each line has exactly 4 columns separated by the pipe `|` character:
   `Date|NY_Report|CA_Report|TX_Report`
   Example line:
   `2023-10-01|System operational, all good!|Minor lag; resolved.|Offline...`

2. **The C Processing Program (`/home/user/process_reports.c`):**
   Write a C program that takes an input filename and an output filename as command-line arguments (e.g., `./process_reports input.dat output.csv`).
   The program must read the wide-format input and output a long-format CSV with the headers: `Date,State,Token`.
   For each region (NY, CA, TX), the program must:
   - Extract the text report.
   - Tokenize the text into individual words. Words are delimited by whitespace and any punctuation characters (e.g., `,`, `.`, `;`, `!`, `?`, `-`).
   - Normalize the words by converting them to lowercase.
   - Ignore empty tokens.
   - Print a line for every valid token in the format: `Date,State,token`. (The State should be exactly `NY`, `CA`, or `TX`).
   
   Using the example above, the output should include:
   ```
   2023-10-01,NY,system
   2023-10-01,NY,operational
   2023-10-01,NY,all
   2023-10-01,NY,good
   2023-10-01,CA,minor
   2023-10-01,CA,lag
   2023-10-01,CA,resolved
   2023-10-01,TX,offline
   ```

3. **Multi-stage & Parallel Pipeline (`/home/user/run_pipeline.sh`):**
   Write a bash script that:
   - Compiles the C program to an executable named `/home/user/process_reports` using `gcc` (ensure it compiles without fatal errors).
   - Creates the directory `/home/user/processed/` if it doesn't exist.
   - Finds all `.dat` files in `/home/user/incoming/` and runs the compiled C program on them **in parallel** (you can use background processes `&` with `wait`, or `xargs -P`).
   - The output for a file named `dayX.dat` should be saved as `/home/user/processed/dayX.csv`. Make sure to output the header `Date,State,Token` at the beginning of each CSV file.

4. **Pipeline Scheduling:**
   Install a cron job for the current user (`user`) that executes `/home/user/run_pipeline.sh` every day at 2:30 AM. 
   Once configured, export the current user's crontab into a file named `/home/user/cron_backup.txt` (e.g., using `crontab -l > /home/user/cron_backup.txt`).

Complete these steps, ensure the bash script has executable permissions, run the script once to process the current files, and export the crontab as requested.