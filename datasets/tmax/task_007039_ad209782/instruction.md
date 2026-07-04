You are an environmental researcher organizing a large dataset of remote sensor telemetry. The data is currently stored in a local SQLite database at `/home/user/telemetry.db`. You need to extract the top telemetry signals for each device, but the queries are currently timing out or running too slowly, and the results need to be strictly validated before they are fed into a downstream NoSQL database.

Your task is to:
1. Identify the missing index strategy for the following analytical query and apply it directly to `/home/user/telemetry.db` using the `sqlite3` CLI. The index should optimize partitioning by `device_id` and sorting by `signal_strength`.
2. Write a C++ program at `/home/user/process_signals.cpp` that connects to the SQLite database using the C API (`<sqlite3.h>`).
3. Have your C++ program execute a query utilizing Window Functions to compute the rank of `signal_strength` (descending) partitioned by `device_id`.
4. Your C++ program must fetch only the top 3 signals (rank <= 3) for each device.
5. Apply schema validation in your C++ code: drop any row where `signal_strength` is missing (NULL) or out of the valid range [-100.0, 0.0]. 
6. Write the validated results to `/home/user/top_signals.csv` in the exact format: `device_id,epoch_sec,signal_strength,rank`. The output must be sorted alphabetically by `device_id`, then by `rank` ascending.

Compile your C++ program to `/home/user/process_signals` and run it so that the CSV file is generated. Ensure that your program handles database connections gracefully and checks for errors. You can compile using `g++ -O2 process_signals.cpp -o process_signals -lsqlite3`.