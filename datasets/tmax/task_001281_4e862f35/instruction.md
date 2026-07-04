You are an AI assistant helping a researcher organize and process a dataset. 

The researcher has a nested archive `/home/user/dataset.tar.gz` containing multiple zip files, each representing an experiment. There is also a configuration file at `/home/user/config.ini` that specifies which experiment and data file needs to be processed.

Your task is to write a Python script at `/home/user/aggregate.py` that does the following:
1. Reads `/home/user/config.ini` to identify the target zip archive and the target CSV file inside it. The config file has the following format:
   ```ini
   [Target]
   zip_file = <name_of_zip_file>
   csv_file = <name_of_csv_file>
   ```
2. Extracts the specified target CSV file from the nested archive (`dataset.tar.gz` -> `<name_of_zip_file>` -> `<name_of_csv_file>`).
3. The CSV file has no header. Calculates the sum of the integers in the second column (index 1) of the extracted CSV file.
4. Appends a line to `/home/user/summary.log` in the exact format: `<zip_file>/<csv_file> SUM:<calculated_sum>`. 
5. To support the researcher running this script across multiple parallel jobs in the future, your script **must** use `fcntl.flock` to acquire an exclusive lock on `/home/user/summary.log` before appending the result, and release it afterward.

After writing the script, execute it once so that `/home/user/summary.log` is generated.