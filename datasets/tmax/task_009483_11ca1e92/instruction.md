I am a researcher organizing some newly collected sensor datasets. I have a nested archive located at `/home/user/research_data.zip`. Inside this zip file are several `.tar.gz` archives, each representing a data chunk.

Inside each `.tar.gz` file, there are two files:
1. `metadata.json`: Contains a JSON object with a `sensor_id` string key.
2. `data.csv`: Contains a CSV with a header. One of the columns is named `reading` (containing numeric values).

Please do the following:
1. Extract `/home/user/research_data.zip` into a directory called `/home/user/extracted_data/`.
2. Write a Python script at `/home/user/aggregator.py` that does the following:
   - Reads a *single* `.tar.gz` file path from standard input (stdin).
   - Extracts the JSON and CSV files from that `.tar.gz` archive (you can do this in memory using the `tarfile` module or in a temporary directory).
   - Parses the `sensor_id` from the JSON.
   - Calculates the sum of all values in the `reading` column of the CSV.
   - Appends the result as a new line to `/home/user/results.csv` in the exact format: `sensor_id,total_sum` (e.g., `sensorA,150.5`).
3. Because I have a massive dataset, I will be processing these files concurrently. Your Python script **must** use `fcntl.flock` to acquire an exclusive lock on `/home/user/results.csv` before writing to it, ensuring that concurrent writes do not corrupt the file.
4. Run your script concurrently on all the `.tar.gz` files you extracted. For example, you can use `find /home/user/extracted_data -name '*.tar.gz' | xargs -n 1 -P 4 bash -c 'echo "$0" | python3 /home/user/aggregator.py'`.

Ensure the final `/home/user/results.csv` is correctly populated with the aggregated data from all archives.