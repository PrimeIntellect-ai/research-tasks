You are tasked with building a high-performance configuration tracking utility in C to detect changes across thousands of server configurations.

We have a configuration management system that dumps the state of all servers daily. You need to write a C program that compares yesterday's dump (`day1.csv`) with today's dump (`day2.csv`) to identify and log all configurations that were added, deleted, or modified. 

The input files are located at:
- `/home/user/configs/day1.csv`
- `/home/user/configs/day2.csv`

Both CSV files have no headers and use the following format:
`server_id,config_key,config_value`
(Example: `server_102,max_connections,500`)

Your C program must:
1. Load and process the two CSV files.
2. Identify changes between `day1.csv` and `day2.csv` using hash-based deduplication and join/merge strategies.
3. Sort the resulting changes alphabetically by `server_id` (ascending), and then by `config_key` (ascending).
4. Output the results to `/home/user/config_delta.csv`.

The output file `/home/user/config_delta.csv` must be a CSV with the following exact format and no header:
`server_id,config_key,STATUS,old_value,new_value`

Where `STATUS` is one of the following:
- `ADDED`: Present in day2 but not day1. (`old_value` must be empty)
- `DELETED`: Present in day1 but not day2. (`new_value` must be empty)
- `MODIFIED`: Present in both, but `config_value` differs.

Examples of expected output rows:
`srv_10,admin_port,MODIFIED,8080,8081`
`srv_10,beta_feature,ADDED,,true`
`srv_12,legacy_mode,DELETED,1,`

Requirements:
- Your source code must be saved as `/home/user/config_tracker.c`.
- Compile it to `/home/user/config_tracker`.
- Execute it to generate the final `/home/user/config_delta.csv`.
- The maximum line length in the CSVs is 256 characters. 
- You may use standard C library functions (e.g., `qsort`, string functions, etc.). No external libraries (like GLib) are installed, so you must implement necessary data structures (like hash tables or sorting routines) yourself.