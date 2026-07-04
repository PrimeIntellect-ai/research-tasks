You are tasked with building a system configuration change tracker in C.

A configuration management system exports periodic snapshots of server configurations in a wide-format CSV file. You need to write a C program that reads this file, standardizes the data, reshapes it, and calculates summary statistics on how often configurations change.

Here is what you need to do:
1. Write a C program located at `/home/user/tracker.c`.
2. The program must read an input CSV file at `/home/user/configs.csv`. 
   The CSV will have a header row and is structured in a wide format: `timestamp,server_id,config1,config2,...`.
   - `timestamp` is an integer (the rows are already sorted by timestamp in ascending order).
   - `server_id` is a string.
   - The remaining columns are configuration keys (the number of config keys can vary, but will not exceed 10).
3. Process the data with the following logic:
   - **Standardization**: Convert all `server_id` values to uppercase.
   - **Reshaping & Tracking**: Conceptually reshape the data into a long format (`timestamp, server_id, config_key, value`) to track changes over time for each `server_id` and `config_key` pair.
   - **Aggregation**: For each unique `server_id` and `config_key`, count the number of times the value changed from one timestamp to the next. The initial value at the first timestamp for a server does *not* count as a change. A change is only counted when a value is different from the chronologically preceding value for that same server and config key.
4. Output the results to `/home/user/changes.csv`.
   - The output must be a headerless CSV with the format: `SERVER_ID,config_key,num_changes`
   - The rows must be sorted alphabetically by `SERVER_ID` (ascending), and then alphabetically by `config_key` (ascending).
5. Compile your C program to an executable at `/home/user/tracker` and run it to produce the final `changes.csv`.

You may only use the standard C library. The input file will not exceed 1000 lines, and line lengths will not exceed 1024 characters.

Example input:
```csv
timestamp,server_id,MaxClients,Timeout,KeepAlive
1,srv-alpha,100,30,on
1,srv-beta,150,60,off
2,srv-alpha,100,45,on
2,srv-beta,200,60,on
3,srv-alpha,150,45,off
3,srv-beta,200,60,on
```

Example expected output (`changes.csv`):
```csv
SRV-ALPHA,KeepAlive,1
SRV-ALPHA,MaxClients,1
SRV-ALPHA,Timeout,1
SRV-BETA,KeepAlive,1
SRV-BETA,MaxClients,1
SRV-BETA,Timeout,0
```