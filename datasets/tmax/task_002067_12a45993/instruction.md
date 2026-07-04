You are tasked with building a configuration management analysis pipeline using **Bash** and standard UNIX utilities (like `awk`, `sort`, `join`, etc.). 

You have been provided with raw logs of configuration changes across a fleet of servers and an inventory file.

**Input Files (You must assume these exist or create a mock to test your script):**
1. `/home/user/config_logs.txt`: Unstructured text logs of config changes.
   Format: `[YYYY-MM-DD] EVENT: config_update HOST: <host_id> PARAM: <parameter_name> VAL: <new_value>`
2. `/home/user/inventory.csv`: A CSV file containing server metadata.
   Format: `host_id,region,environment`

**Your Goal:**
Write a Bash script at `/home/user/analyze_configs.sh` that processes these files and generates two specific analytical reports in the `/home/user/output/` directory.

**Requirements for the Script:**
The script must perform the following data processing steps and produce exactly two output files. Ensure the output directory is created if it doesn't exist.

**Output 1: Daily Region Rolling Average (`/home/user/output/daily_region_stats.csv`)**
1. Extract the date, host, and parameter from the logs.
2. Join this data with the inventory file to determine the region for each change.
3. Group the data to calculate the total number of configuration changes *per day, per region*.
4. Calculate a **2-day rolling average** of the total changes for each region (i.e., the average of the current day's total and the previous day's total. If there is no previous day in the dataset for that region, the rolling average is just the current day's total).
5. The output CSV must have a header and be sorted chronologically by date, then alphabetically by region.
   *Format:* `date,region,daily_total,rolling_avg` (Format rolling_avg to 1 decimal place, e.g., 2.0 or 3.5).

**Output 2: Host Similarity Analysis (`/home/user/output/host_similarity.csv`)**
We want to find which hosts have similar configuration change profiles.
1. Filter the dataset to only include hosts in the `us-east` region.
2. For each host, calculate its "configuration profile": the count of updates it made to each distinct parameter across all dates.
3. Compute the **Manhattan Distance** between all unique pairs of `us-east` hosts based on their configuration profiles. (The Manhattan distance is the sum of the absolute differences of their update counts for every parameter that either host has updated).
4. Output the pairs and their distance. Ensure `host1` is alphabetically strictly less than `host2` (e.g., `app-01,web-01`, not `web-01,app-01`).
5. Sort the output alphabetically by `host1`, then `host2`.
   *Format:* `host1,host2,manhattan_distance` (No header required).

Make sure your script `/home/user/analyze_configs.sh` is executable and can be run without arguments to automatically process the files at `/home/user/config_logs.txt` and `/home/user/inventory.csv` and write to `/home/user/output/`.