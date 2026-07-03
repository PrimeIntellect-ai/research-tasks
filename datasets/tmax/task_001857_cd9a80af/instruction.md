You are tasked with implementing a configuration manager's custom backup process. 

In the `/home/user/configs/` directory, there are several `.conf` files. 
There is also a deployment log file at `/home/user/changes.log` which tracks updates to these files across different commits.

Your objectives are:
1. **Multi-line Log Parsing & Incremental Backup**: Parse `/home/user/changes.log`. The log contains multi-line entries for each commit. Identify the files modified in the **last** (most recent) commit at the bottom of the log. You only need to back up these specific files.
2. **Format Conversion & Renaming**: The `.conf` files are in a simple `key=value` text format (one per line). Convert the content of the modified files into valid JSON objects (e.g., `{"key": "value"}`). Save these JSON files into a newly created `/home/user/backup/` directory. When saving, rename the files by prepending `backup_` and changing the extension to `.json` (e.g., `network.conf` becomes `backup_network.json`).
3. **Custom Compression**: We use a text-safe archive format. Create a compressed gzip tarball (`.tar.gz`) containing only the JSON files inside the `/home/user/backup/` directory (do not include the parent `backup` directory path in the tarball itself). Then, Base64 encode the entire tarball.
4. Save the final Base64 string to `/home/user/archive.b64`.

Everything must be done dynamically based on the contents of the log file and the configs. Ensure your output JSON is properly formatted (strings for both keys and values are fine).