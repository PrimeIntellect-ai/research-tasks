You are tasked with identifying an anomaly in a stream of configuration updates.

A configuration manager tracks changes across a fleet of servers. Every update is logged into a large, tab-separated values (TSV) file located at `/home/user/config_updates.tsv`. 

The file has four columns:
1. `Date` (YYYY-MM-DD format)
2. `ServerID` (String)
3. `ConfigKey` (String)
4. `ConfigValue` (UTF-8 encoded string, potentially containing multi-language text)

We suspect that a rogue script recently pushed extremely long Message Of The Day (`MOTD`) configurations. We need to find the exact date this happened using mathematical changepoint detection (specifically, finding the maximum absolute day-to-day difference in the average character length).

Your objective is to:
1. Filter the dataset to only include rows where `ConfigKey` is `MOTD`.
2. For each day, calculate the average length (in **Unicode characters**, NOT bytes) of the `ConfigValue` strings.
3. Sort the days chronologically.
4. Calculate the absolute difference in the average character length between each day and its immediate chronological predecessor in the filtered log.
5. Identify the day (the later day in the pair) with the maximum absolute difference.
6. Write the result to `/home/user/anomaly_report.txt` in the exact format: `YYYY-MM-DD,DiffValue` where `DiffValue` is rounded to 2 decimal places.

For example, if the average MOTD lengths were:
- 2024-01-01: 5.00
- 2024-01-02: 8.50 (Diff: 3.50)
- 2024-01-03: 25.50 (Diff: 17.00)
- 2024-01-04: 20.00 (Diff: 5.50)
The changepoint is `2024-01-03`, and the output should be `2024-01-03,17.00`.

Requirements:
- You must use Python to compute the character lengths and averages, but you can use bash utilities (like `grep`, `awk`) for initial filtering.
- Handle the file efficiently. 
- Ensure you measure Unicode characters accurately (e.g., "こんにちは" is 5 characters, even though it takes 15 bytes).

Place your final answer in `/home/user/anomaly_report.txt`.