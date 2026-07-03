You are an AI assistant helping a configuration manager track the actual deployed state of configurations across a fleet of servers. 

A central logging service dumps raw, noisy configuration change events into a local text file: `/home/user/config_updates.log`. 

The log file contains entries in this exact format:
`[YYYY-MM-DD HH:MM:SS] <SERVER_ID> <CONFIG_KEY>=<VALUE>`

Example:
`[2023-10-15 08:32:11] srv-alpha DB_TIMEOUT=30`
`[2023-10-15 08:35:00] srv-beta MAX_CONNS=100`
`[2023-10-15 08:36:15] srv-alpha DB_TIMEOUT=45`

The file is chronologically ordered but contains noise, including exact duplicate lines and overridden configurations (where a key's value is updated later for the same server).

Your task:
1. Write a C program at `/home/user/track_config.c`.
2. The program must read `/home/user/config_updates.log` and extract the structured information.
3. It must clean and deduplicate the data by determining the *latest* configuration state (the last seen value) for every unique `(SERVER_ID, CONFIG_KEY)` pair.
4. The program must output the final deduplicated configuration state to a CSV file at `/home/user/latest_configs.csv`.
5. The output CSV must have the header `server,key,value` and the rows must be sorted alphabetically by `server`, then by `key`.
6. Compile the C program to `/home/user/track_config` using `gcc` and run it to generate the CSV.

Constraints:
- You may assume there are no more than 1000 unique `(SERVER_ID, CONFIG_KEY)` combinations.
- No line in the log file exceeds 256 characters.
- SERVER_ID, CONFIG_KEY, and VALUE consist of alphanumeric characters, hyphens, and underscores only. No spaces inside them.

Once you have written, compiled, and executed the C program to generate `/home/user/latest_configs.csv`, your task is complete.