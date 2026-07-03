You are tasked with building a C++ tool to process a large stream of configuration change events for our system. The configuration events are logged in a text file, and we need to extract the latest state of each configuration key, count the number of unique values each key has been assigned, and perform a rolling hourly aggregation of changes.

**Input Format:**
You will be processing a file located at `/home/user/config_events.txt`.
Each line in the file represents a single configuration change event, delimited by the pipe character `|`.
The format is: `timestamp|user|action|config_key|config_value`
- `timestamp`: An integer representing the UNIX epoch time in seconds.
- `user`: The user who made the change.
- `action`: The type of action (e.g., CREATE, UPDATE, DELETE).
- `config_key`: The name of the configuration setting.
- `config_value`: The value assigned to the configuration.

**Requirements:**
1. Write a C++ program at `/home/user/config_tracker.cpp` and compile it to `/home/user/config_tracker`. It should take two arguments: the input file path and the output directory path. (e.g., `./config_tracker /home/user/config_events.txt /home/user/output/`)
2. **Streaming:** Process the file line-by-line to avoid loading the entire file into memory (assume the file could be larger than available RAM).
3. **Normalization:** Tokenize the line. Extract the `config_key` and normalize it by converting it to lowercase and replacing any non-alphanumeric character (anything not `a-z` or `0-9`) with an underscore `_`.
4. **Deduplication & State Tracking:** Maintain the *latest* `config_value` for each normalized `config_key` based on the order of appearance in the file (assume the file is chronological). Also, use a hash-based mechanism to count the number of *strictly unique* values each normalized key has been assigned over the entire file.
5. **Windowed Aggregation:** Calculate the total number of events that occurred in each 1-hour tumbling window. A 1-hour window starts at a timestamp divisible by 3600. For example, timestamp 1600000000 falls into the window 1600000000, timestamp 1600001800 falls into 1600000000, and 1600004000 falls into 1600003600.
6. Create the output directory if it doesn't exist.

**Output:**
The program must generate two CSV files in the output directory:

1. `latest_configs.csv`
Format: `normalized_key,latest_value,unique_values_count`
This file must be sorted alphabetically by `normalized_key`.

2. `hourly_counts.csv`
Format: `window_start_epoch,change_count`
This file must be sorted numerically by `window_start_epoch` in ascending order.

After writing and compiling the program, execute it on `/home/user/config_events.txt` with the output directory `/home/user/output`.