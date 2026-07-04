You are tasked with normalizing and gap-filling a stream of configuration change events. An upstream ETL job tracks configuration changes but occasionally produces duplicate records on retry, and the events arrive irregularly. We need to create a uniform, downsampled timeline of changes.

You have been provided with a CSV file at `/home/user/config_events.csv`.
The file is sorted by timestamp and has the format: `timestamp,category,change_desc`

The valid categories are exactly three: `DB`, `NET`, and `SEC`.

Write a C program at `/home/user/process_configs.c` (and compile it to `/home/user/process_configs`) that processes this file in a streaming fashion (do not load the entire file into memory at once). The program must write to `/home/user/normalized_configs.csv` following these rules:

1. **Windowing:** Group the events into fixed 60-second time windows. The first window starts at `W_start = first_timestamp - (first_timestamp % 60)`, where `first_timestamp` is the timestamp of the very first event in the file. Subsequent windows start at `W_start + 60`, `W_start + 120`, etc.
2. **Sampling & Deduplication:** For each 60-second window `[W, W+60)`, you must output exactly ONE record per category. Take the *first* event that appears for a category in that window. Ignore any subsequent events (which handles the ETL duplicates) for that category in the same window.
3. **Gap-filling:** If a 60-second window completes and one or more categories had *no* events, you must generate a synthetic record for each missing category with the description `NO_CHANGE`.
4. **Empty Windows:** If one or more entire 60-second windows pass with zero events before the next event arrives, you must generate `NO_CHANGE` records for all three categories for those empty windows.
5. **Termination:** Stop processing after generating outputs for the window that contains the very last event in the input file.
6. **Output Format:** The output must be written to `/home/user/normalized_configs.csv` in the format `window_start_timestamp,category,change_desc`.
7. **Sorting:** Within each 60-second window in the output file, the three categories must be printed in alphabetical order: `DB`, `NET`, `SEC`.

Example:
If the first event is at `1700000005`, the first window is `[1700000000, 1700000060)`.
If only `NET` has an event ("fw_update") in that window, the output for that window must be:
1700000000,DB,NO_CHANGE
1700000000,NET,fw_update
1700000000,SEC,NO_CHANGE