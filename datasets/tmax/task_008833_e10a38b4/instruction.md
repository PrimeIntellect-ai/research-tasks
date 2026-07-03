You are helping a climate researcher process a large set of raw environmental measurements. 

The researcher has provided you with a compressed archive located at `/home/user/data/raw_measurements.tar.gz`. Inside this archive, there is a directory called `measurements` which contains data in two different formats:
1. **JSON files** (`*.json`): These contain arrays of objects. Each object has keys: `"timestamp"`, `"station_id"`, `"temperature"`, and `"humidity"`.
2. **CSV files** (`*.csv`): These contain tabular data with a header row: `timestamp,station_id,temperature,humidity`.

Your task is to:
1. Extract the archive.
2. Search through all the JSON and CSV files to find all records where the `temperature` is **greater than or equal to 40.0**.
3. Combine these anomalous records into a new CSV file located at `/home/user/data/anomalies.csv`. 
4. The `anomalies.csv` file must have exactly two columns with the header: `station,temp`.
5. The rows in `anomalies.csv` (excluding the header) must be sorted alphabetically by the `station` column (ascending), and then numerically by the `temp` column (descending).
6. Finally, package and compress this single `anomalies.csv` file into a new gzip-compressed tar archive located at `/home/user/data/anomalies.tar.gz`. The archive should contain only the `anomalies.csv` file (no nested directories).

Use standard bash CLI tools (`tar`, `jq`, `awk`, `sort`, etc.) to complete this task.