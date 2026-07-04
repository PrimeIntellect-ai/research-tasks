You are managing configuration versions for multiple servers over time. You have been provided with a time-series history of configuration versions in a "wide" CSV format, but you need to reshape this data, generate human-readable tracking reports using a specific template, and archive them to a remote backup directory.

The input data is located at `/home/user/config_history.csv` with the following format:
```csv
Date,AppServer,DbServer,WebCache
2023-10-01,v1.2,v9.1,v2.0
2023-10-02,v1.3,v9.1,v2.1
2023-10-03,v1.3,v9.2,v2.1
```

Your tasks are:
1. Write a C program at `/home/user/process_configs.c` that reads `/home/user/config_history.csv`.
2. The program must reshape the data (logically converting wide to long format) to group the history by each server.
3. For each server (excluding the "Date" column header), the program must generate a text report file in the current directory named `<ServerName>.report` (e.g., `AppServer.report`).
4. The generated report MUST strictly match the following template format:
   ```text
   REPORT FOR: <ServerName>
   ========================
   Update History:
   - <Date>: <Version>
   - <Date>: <Version>
   ...
   ```
   (List the dates in the same order they appear in the CSV).
5. Compile your C program using standard `gcc` and run it.
6. Transfer (copy or move) all the generated `.report` files to the mounted remote backup directory at `/home/user/remote_archive/`.

Ensure the output formatting is exact, including capitalization and whitespace. Do not include any empty lines at the end of the file unless specified.