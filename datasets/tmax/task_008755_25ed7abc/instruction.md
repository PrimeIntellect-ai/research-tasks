You are acting as a storage administrator who needs to reclaim disk space across a fleet of servers. The monitoring system has dumped the disk usage logs for several servers into a single nested archive, but the data is in mixed formats.

Your task is to analyze these logs and identify the top 5 largest files across all servers.

**Environment Details:**
You have been provided with an archive located at: `/home/user/logs/server_usage.tar.gz`

Inside this tarball, there are several directories (representing different servers). Inside each server directory, there are one or more `.zip` files containing the actual log data.
Inside the `.zip` files, there are files in two formats:
1. `.json` files containing arrays of objects: `[{"file_path": "/some/path", "size_bytes": 1024}, ...]`
2. `.csv` files with a header and rows: `file_path,size_bytes`

**Requirements:**
1. Using **Python**, write a script or set of commands to extract and parse all this nested data. You may extract the archives to disk or process them in memory.
2. Aggregate all the file entries from all `.json` and `.csv` files across all servers.
3. Identify the 5 files with the largest `size_bytes` across the entire dataset.
4. Output this top 5 list to a JSON file at `/home/user/top_5_hogs.json`.
5. The output must be a valid JSON array of objects, sorted in **descending order** by `size_bytes`. If two files have the exact same size, sort them alphabetically by `file_path` in ascending order.
6. The output JSON format must exactly match this structure:
   ```json
   [
     {
       "path": "/exact/file/path",
       "size": 123456789
     },
     ...
   ]
   ```
   *(Note the keys in the output are `"path"` and `"size"`, converted from the input keys `"file_path"` and `"size_bytes"`).*

Ensure your final result is placed exactly at `/home/user/top_5_hogs.json`.