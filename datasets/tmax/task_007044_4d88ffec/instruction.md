You are an AI assistant tasked with building a configuration tracker in Go that processes a series of nested backup archives. 

You need to write and execute a Go program that acts as a configuration manager tracking changes across daily backups. The system administrator left a configuration file at `/home/user/config.json` that dictates which backups to process. 

Your Go program must fulfill the following requirements:
1. Parse `/home/user/config.json`. This file contains:
   - `backups`: A list of objects with `name` and `path` (pointing to archive files).
   - `track_file`: The name of the configuration file you need to find inside the archives (e.g., `app.conf`).
   - `max_depth`: An integer specifying the maximum allowed archive nesting depth. 
   - `output`: The path where you must write the final JSON report.

2. Process each backup archive defined in the config. Archives can be either `.tar.gz` or `.zip` formats.
   - Archives may contain the `track_file` directly, OR they may contain nested archives (e.g., a `.zip` inside a `.tar.gz`).
   - You must search for `track_file` even inside nested archives by processing the compressed streams.
   - **Crucial Rule:** To prevent infinite loops caused by malicious nested archives (archive bombs) or recursive symlinks, you must track the nesting depth. 
     - The top-level archive specified in `config.json` is at `depth = 0`.
     - An archive inside the top-level archive is at `depth = 1`, and so on.
     - If you encounter an archive that would exceed `max_depth`, you must immediately stop processing that specific top-level backup and mark it with an error.

3. Extract the `version` value from the `track_file`. The `track_file` is a plain text file containing key-value pairs separated by `=` (e.g., `version=1.2.3`).

4. Write a JSON report to the file specified in the `output` field of `config.json`. The output must be a single JSON object where the keys are the `name` of the backups, and the values are objects containing:
   - `version`: The extracted version string (or an empty string if there was an error).
   - `status`: `"ok"` if the file was found and parsed successfully, or `"error_depth_exceeded"` if the nesting depth exceeded `max_depth`. If the file is simply not found within valid depths, use `"error_not_found"`.

Example expected output format for `/home/user/report.json`:
```json
{
  "backup_mon": {
    "version": "1.0",
    "status": "ok"
  },
  "backup_tue": {
    "version": "",
    "status": "error_depth_exceeded"
  }
}
```

Write the Go code, build it, and run it to produce the final `/home/user/report.json`.