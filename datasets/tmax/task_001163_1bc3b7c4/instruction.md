You are a backup administrator managing server archive data. 

There is an incoming compressed backup file located at `/home/user/incoming_backup.tar.gz`. Inside this archive is a single JSON file named `data.json`, which contains an array of backup log objects. 

Your task is to write a single bash command (or a short bash script) that does the following:
1. Reads the `data.json` stream directly from the compressed archive *without* extracting the file to disk.
2. Parses the JSON data to extract the `server_id`, `timestamp`, and `backup_size` fields from each object.
3. Converts the extracted data into CSV format (comma-separated).
4. Safely appends these CSV rows to a master archive file located at `/home/user/backup_summary.csv` using file locking (`flock`) to prevent race conditions during the append operation.

The master archive file `/home/user/backup_summary.csv` already exists and contains a header: `server_id,timestamp,backup_size`. Do not add a duplicate header.

You may use Python (e.g., as a one-liner or short script), `jq`, `tar`, `flock`, and standard bash utilities to accomplish this. 

Ensure that your final append operation is locked using file descriptor 200 on `/home/user/backup_summary.csv`. For example: `flock 200` associated with the append redirection.