You are a storage administrator managing a nearly full server. A legacy application dumped a large compressed archive of mixed telemetry, configuration, and binary state files before crashing. You need to analyze the contents of this archive to identify corrupted states and legacy configurations so you can determine what data is safe to purge.

The archive is located at `/home/user/storage/telemetry_dump.tar.gz`. 

Inside the compressed archive, there is a flat directory structure containing three types of files:
1. **Log files (`*.log`)**: These are CSV formatted. The columns are `timestamp,hostname,error_code,message`.
2. **Metadata files (`*.meta`)**: These are JSON formatted. They contain keys like `{"id": "...", "version": 1.5, "size": 1024}`.
3. **State files (`*.bin`)**: These are custom binary files. The first 4 bytes represent a magic number (unsigned 32-bit integer, big-endian). The next 4 bytes represent the file version (unsigned 32-bit integer, little-endian). The rest of the file is raw payload data.

Your task is to analyze the archive and extract specific metrics. To save disk space, you may extract the files, but your final output must be a single summary file.

Please generate a JSON report at `/home/user/storage_report.json` with the following exact structure and keys:
```json
{
  "critical_error_count": <integer: total number of .log files that contain AT LEAST ONE row with an error_code strictly greater than 500>,
  "legacy_meta_ids": [<array of strings: the "id" values from all .meta files where the "version" is strictly less than 2.0. MUST BE SORTED ALPHABETICALLY>],
  "target_bin_count": <integer: total number of .bin files where the magic number is EXACTLY 0xDEADC0DE and the version is EXACTLY 3>
}
```

Constraints and tips:
- You can use any programming language available in the environment (e.g., Python, Bash, Perl) to write your analysis script.
- Ensure the JSON file is properly formatted.
- The `legacy_meta_ids` array must be sorted in alphabetical order.