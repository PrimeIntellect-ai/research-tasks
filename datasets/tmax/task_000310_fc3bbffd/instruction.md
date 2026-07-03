You are tasked with building a configuration state tracking tool in C. We have a set of servers that stream delta configuration changes (long format) over a 24-hour period. We need to reconstruct the wide-format state of all servers at the end of each hour bucket.

First, extract the base configuration from an image provided at `/app/base_config.png`. This image contains a typed table of the initial starting values for each server's parameters before any deltas are applied (at time < 1672531200). Use OCR (like `tesseract`) to read it.

Second, process the delta logs located at `/home/user/data/deltas.csv`. The deltas are in a long format: `timestamp,server_id,param_name,new_value`.

Write a C program that:
1. Accepts the parsed base configurations and the `deltas.csv` data.
2. Sorts or joins the changes to reconstruct the timeline of states.
3. Groups the time into 1-hour buckets. Hour index `0` covers timestamps `[1672531200, 1672534799]`, hour `1` covers `[1672534800, 1672538399]`, etc., up to hour `23`.
4. Determines the final state of each parameter for each server at the *end* of each hour bucket. If a parameter didn't change during an hour, its value carries over from the previous hour (or the base configuration).
5. Reshapes the data into a wide format and outputs it to `/home/user/hourly_summary.csv`.

The output CSV must have the exact header:
`hour_index,ALPHA_fan_speed,ALPHA_temp_limit,BETA_fan_speed,BETA_temp_limit`
Followed by 24 rows (0 to 23) containing the floating-point values of the parameters at the end of that hour bucket.

Requirements:
- Your core data processing and reshaping logic MUST be written in C. You can use bash/python for the OCR wrapper and compiling/running the C code, but the joining, wide-long reshaping, and bucketing must be in C.
- Write your C code to `/home/user/tracker.c` and compile it to `/home/user/tracker`.
- Ensure output floats are formatted to 1 decimal place.