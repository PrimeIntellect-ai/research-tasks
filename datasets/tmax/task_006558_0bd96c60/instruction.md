You are managing the configuration drift monitoring system for a distributed application. Daily drift scores (representing how far a service's configuration has deviated from the baseline) are exported as wide-format CSV files from different regions. 

Your task is to write a Bash script at `/home/user/process_drift.sh` that processes these files and schedule it to run automatically.

Requirements for `/home/user/process_drift.sh`:
1. Look for all `.csv` files inside `/home/user/reports/`.
2. Use standard Linux CLI tools (`awk`, `sed`, `xargs`, etc.) to process the files **in parallel** (e.g., using `xargs -P` or parallel).
3. Reshape the data conceptually from wide format (`service_name, score_day1, score_day2, ...`) into a stream of `service_name, score` pairs.
4. **Validation and Cleaning Checkpoint**: 
   - Trim any leading/trailing whitespace from service names and scores.
   - Discard any scores that are empty, not valid positive numbers, or negative numbers.
   - Ignore header rows (the first row of each file, which starts with `service_name`).
5. Calculate the total mathematical sum of valid drift scores for each `service_name` across all files.
6. Write the top 3 services with the highest total drift to `/home/user/top_drifts.txt`. The output must be formatted exactly as `service_name:total_score` (scores formatted to 1 decimal place, e.g., `ServiceA:15.5`), sorted in descending order of the total score.

After creating and testing the script, add a cron job for the `user` that runs `/home/user/process_drift.sh` every day at 2:00 AM.

Ensure your script is executable (`chmod +x`). Use only bash built-ins and standard coreutils/GNU tools. Do not use Python, Perl, or other scripting languages.