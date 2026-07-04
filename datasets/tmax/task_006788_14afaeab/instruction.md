You are a Configuration Manager building a reporting pipeline to track configuration changes across multiple servers. 

Currently, server configuration logs are dumped into an incoming directory: `/home/user/upstream_configs/`.
Your task is to transfer these files, normalize the data, and compute rolling statistics using only Bash and standard command-line tools (like `awk`, `sed`, `grep`, `sort`, etc.). No Python, Perl, or other scripting languages are allowed.

**Step 1: Local-Remote Transfer Simulation**
Copy all `.csv` files from `/home/user/upstream_configs/` to a new working directory at `/home/user/local_configs/`.

**Step 2: Normalization and Standardization**
The CSV files contain configuration change logs with three columns: `Date,ConfigFile,LinesChanged`.
However, the data is messy:
- Dates are inconsistently formatted as either `YYYY-MM-DD` or `MM/DD/YYYY`.
- `ConfigFile` names have inconsistent capitalization (e.g., `Nginx.conf` vs `nginx.conf`).
- There is extra whitespace around fields.

Create a normalized, consolidated file at `/home/user/normalized_changes.csv` that contains the data from all files.
Rules for normalization:
- All dates must be in `YYYY-MM-DD` format.
- All `ConfigFile` names must be entirely lowercase.
- All leading and trailing whitespace from every field must be removed.
- The output should be a comma-separated file: `Date,ConfigFile,LinesChanged`

**Step 3: Rolling Aggregation and Statistics**
Using the normalized data, calculate the daily total of `LinesChanged` across all configuration files, and then compute a 3-record rolling average of these daily totals.

Rules for aggregation:
- Group the data by `Date` and sum the `LinesChanged`.
- Sort the aggregated data chronologically.
- Calculate a 3-record rolling average (the average of the current day's total and up to 2 preceding days' totals). Note: use the sequence of available dates in the file, regardless of whether there are gaps in the calendar days.
- Format the rolling average to exactly one decimal place (e.g., `20.0`, `18.3`).

Write the final results to `/home/user/rolling_averages.csv` with the following format:
`Date,DailyTotal,Rolling3DayAvg`

For example, a valid row in the final file might look like:
`2023-10-03,28,23.3`