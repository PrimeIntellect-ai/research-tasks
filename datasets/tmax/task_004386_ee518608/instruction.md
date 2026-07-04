You are an IT support technician handling an escalated ticket (Ticket #1029). 

The billing department reports that their nightly aggregation pipeline is failing. The pipeline is supposed to calculate the total cloud usage costs across all servers by summing the `cost` values in the daily logs. However, the system is crashing on some files, and when they try to bypass the crash, the final total is a massive negative number due to corrupted records.

Your task is to debug the dataset and compute the correct final billing amount using standard terminal tools.

Here are the specifics:
1. The raw logs are located in `/home/user/ticket_1029/data/`. There are 100 CSV files (named `file_001.csv` through `file_100.csv`).
2. Each file does not have a header. The format is: `server_id,timestamp,cpu_usage,cost`. The `cost` is the 4th column (a floating-point number).
3. Exactly **two** files are corrupted:
   - One file contains a massive negative outlier in the cost column (a numerical corruption issue) that severely skews the total sum.
   - One file contains an unparseable/malformed string in the cost column (e.g., an error code instead of a number), which breaks standard shell math tools.
4. You must find these two specific problematic files.
5. Once identified, create a log file at `/home/user/ticket_1029/bad_files.txt`. Write the exact base names of the two corrupted files (e.g., `file_005.csv`), one per line, sorted alphabetically.
6. Calculate the total sum of the `cost` column for all **98 valid files** (completely excluding the two corrupted files).
7. Save the final sum, formatted to exactly two decimal places (e.g., `1540.50`), to `/home/user/ticket_1029/correct_total.txt`.

You may write any helper scripts in Bash, Awk, Python, or another language of your choice to trace the intermediate states, isolate the bad files via delta debugging, and compute the correct sum.