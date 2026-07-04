You are acting as a configuration manager for a system that receives automated backups. Over time, some backup archives have been corrupted due to a bug in a log rotation script that races with the backup writing process. 

Your task is to process a directory of backup archives, verify their integrity, extract the configuration files from the valid ones, convert them from JSON to YAML format, and consolidate them into a single tracking file.

Specifically, you need to write and execute a Python script that does the following:
1. Iterates through all `.zip` and `.tar.gz` files in the directory `/home/user/backups/` in alphabetical order.
2. Verifies the integrity of each archive. If an archive is corrupted or invalid, skip it and append its filename (just the basename, e.g., `backup_03.tar.gz`) to `/home/user/corrupted.log`.
3. For valid archives, extract the file named `config.json` contained within.
4. Convert the JSON content to YAML format.
5. Append the YAML output to `/home/user/all_configs.yaml`. Immediately before the YAML content for each archive, insert a comment line in the format: `# Source: <filename>` (e.g., `# Source: backup_01.zip`). 
6. When converting to YAML using the `pyyaml` library, use `yaml.dump` with `default_flow_style=False` and `sort_keys=True` to ensure consistent formatting. You may need to install `pyyaml` via pip.

Ensure your script handles exceptions gracefully to identify corrupted files without crashing.