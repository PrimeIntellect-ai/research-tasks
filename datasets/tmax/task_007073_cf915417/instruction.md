You are a developer tasked with organizing some legacy project files that have lost their file extensions.

In the directory `/home/user/data_dumps/`, there are several files named `dump_01`, `dump_02`, up to `dump_10`. Some of these files are standard text files, some are random binary data, and some are valid GZIP archives (which can be identified by their standard `1F 8B` magic bytes). 

Your task is to:
1. Identify which of the files in `/home/user/data_dumps/` are valid GZIP archives.
2. Decompress these valid GZIP archives. Each valid GZIP file contains a single JSON array of objects.
3. Parse the JSON data from all the valid archives. Look for objects where the `"category"` key is exactly `"database"`.
4. Extract the `"mount_path"` value from these specific objects.
5. Create a CSV file at `/home/user/database_mounts.csv` containing all the extracted mount paths. The CSV must have a single header `path` and the paths should be listed in alphabetical order, one per line.

Do not manually guess the file types; use programmatic methods or standard utilities to identify the archives based on their binary headers.