I need your help processing some configuration exports from our server fleet. 

We have a CSV file located at `/home/user/data/configs.csv` containing server configuration backups. The file has three columns: `server_id`, `timestamp`, and `raw_config`. 

Because the `raw_config` field contains multiline text (embedded newlines inside quotes), standard bash line-by-line tools are failing to process it correctly. 

Please write and execute a Python script that does the following:
1. Safely parses the CSV file, correctly handling the embedded newlines.
2. Normalizes the `raw_config` string for each server by converting it entirely to lowercase and removing absolutely all whitespace characters (spaces, tabs, newlines, carriage returns).
3. Computes the SHA-256 hex digest of the normalized configuration string.
4. Groups the `server_id`s by this SHA-256 hash to deduplicate the configurations.
5. Sorts the list of `server_id`s alphabetically for each hash group.
6. Saves the result to `/home/user/output/grouped_configs.json` as a JSON object where the keys are the SHA-256 hashes and the values are the sorted lists of `server_id` strings.

Make sure the output directory exists before writing to it.