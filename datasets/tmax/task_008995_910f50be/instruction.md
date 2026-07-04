You are a storage administrator tasked with automating the processing of disk usage reports. To manage disk space efficiently, you need a service that watches for new disk usage reports, filters for servers with critical disk usage, and splits the data into small, manageable chunks for a legacy archiving system.

Write a Go program located at `/home/user/watcher.go` that does the following:
1. Uses `github.com/fsnotify/fsnotify` to monitor the directory `/home/user/incoming/` for new file `CREATE` events.
2. When a `.csv` file is created in this directory, it should parse the CSV file. The CSV files will always have a header row and the following columns: `Hostname,DiskSizeGB,UsedGB,Status`.
3. Filter the rows to include ONLY servers where `UsedGB` is strictly greater than `80`.
4. Convert the filtered rows into JSON objects with the schema: `{"hostname": "...", "used_gb": <int>}`. Note that `used_gb` must be an integer.
5. Chunk these JSON objects into arrays of exactly 2 objects each (the final chunk may contain fewer if there's a remainder).
6. Save these JSON arrays to the `/home/user/processed/` directory with the naming convention `chunk_1.json`, `chunk_2.json`, etc., for each processed file. Start counting at 1 for each new CSV file processed. 

Once your code is written:
1. Initialize a Go module in `/home/user/` and install any necessary dependencies.
2. Build and run your Go program in the background.
3. Simulate a report arrival by copying the pre-existing file `/home/user/raw_data.csv` to `/home/user/incoming/report.csv`.
4. Wait for your program to process the file and generate the chunks in `/home/user/processed/`.
5. Once the `chunk_*.json` files appear, you may exit.

Do not remove the generated chunk files.