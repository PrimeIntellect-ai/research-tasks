You are a storage administrator tasked with managing disk space on a shared server. Users have been trying to bypass quota restrictions by uploading large compressed archives and giving them deceptive extensions like `.txt`, `.log`, or `.dat`.

Your task is to identify these hidden archives by reading file headers (magic bytes) and generate a report based on a configuration file.

1. Read the configuration file located at `/home/user/scan_config.ini`. This file contains the target directory to scan and the output report path.
2. Scan all files in the target directory specified in the configuration.
3. Determine the actual file type by checking the first few bytes (magic numbers) of each file. You are looking specifically for:
   - GZIP archives (starts with `1F 8B` in hex)
   - ZIP archives (starts with `50 4B 03 04` in hex)
4. Create a report of all hidden archives found. The report must be saved to the path specified by the `report_path` key in the configuration file.
5. The report must contain exactly one line per hidden archive found, sorted alphabetically by the full file path.
6. Each line in the report must strictly follow this format:
   `[FULL_FILE_PATH]|[ARCHIVE_TYPE]|[SIZE_IN_BYTES]`
   Where `[ARCHIVE_TYPE]` is either `GZIP` or `ZIP`.

You should use Python to create a script that reads the configurations, inspects the binary headers, and writes the formatted log.

Do not include files that are actually plain text or other formats, even if they have weird extensions.