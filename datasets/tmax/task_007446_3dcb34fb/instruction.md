You are acting as a backup administrator for a Linux-based application server. 

Your task is to securely archive a specific set of configuration and log files based on a backup plan, ensuring that sensitive data is redacted before archiving, and generating an integrity manifest.

Here are your instructions:
1. Read the master backup plan located at `/home/user/server_data/backup_plan.json`. This JSON file contains a key `"targets"` which is a list of objects. Each object has a `"file"` key (a relative path from `/home/user/server_data/`) and a `"redact"` key.
2. For each file in the plan:
   - Read the file from `/home/user/server_data/<file_path>`.
   - If the `"redact"` value is `"ipv4"`, you must replace all valid IPv4 addresses in that file with the exact string `[REDACTED]`. You can use command-line tools like `sed` or `awk`, or handle it within a Python script.
   - If the `"redact"` value is `"none"`, leave the content unchanged.
3. You must safely stage these processed files. Use atomic writes (e.g., write the processed content to a temporary file first, then atomically move/rename it to a staging directory) to ensure no partial files are created if a process gets interrupted.
4. Create a compressed tarball named `/home/user/safe_backup.tar.gz` containing only the processed target files. The files inside the tarball should maintain their relative paths (e.g., `logs/access.csv` and `conf/settings.xml` should be at the root of the archive). Do not include the `server_data` parent directory itself in the archive paths.
5. Create a CSV manifest of the archived (and potentially redacted) files at `/home/user/manifest.csv`. The CSV must have exactly two columns with headers: `file_path,sha256_hash`. The `file_path` must match the relative path inside the archive (e.g., `logs/access.csv`), and the `sha256_hash` must be the SHA256 checksum of the *processed* file. Sort the CSV rows alphabetically by `file_path`.

Write and execute the necessary Python scripts and shell commands to accomplish this. Ensure that files not listed in `backup_plan.json` are strictly ignored.