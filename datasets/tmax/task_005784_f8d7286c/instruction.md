You are acting as a backup administrator recovering specific data from a fragmented and poorly packaged backup archive. 

You must perform the following steps to extract the data and generate a recovery report:

1. **Reassemble and Extract**: In `/home/user/backups/`, there is a split archive named `split_archive.tar.gz.aa`, `split_archive.tar.gz.ab`, etc. Recombine these parts into a single `tar.gz` archive and extract its contents into `/home/user/extracted/`.
2. **Safe Extraction (Flattening)**: Inside the extracted contents, you will find a tar file named `configs.tar`. This archive contains configuration files buried under deep and potentially unsafe relative directory paths. You must extract ONLY the `.conf` files from `configs.tar` directly into a new directory `/home/user/safe_configs/`, completely ignoring and removing any directory structure (flatten the files into the single `safe_configs` directory).
3. **Bulk Renaming**: The extracted files in `/home/user/safe_configs/` all have an `old_` prefix and a `.conf` extension (e.g., `old_name.conf`). Rename all of them in bulk to remove the `old_` prefix and change the extension to `.ini` (so `old_name.conf` becomes `name.ini`).
4. **Configuration Parsing**: In `/home/user/extracted/`, there is a file named `rules.txt` containing mapping rules in the format `filename:key`. For each rule, locate the corresponding renamed file in `/home/user/safe_configs/`. The `.ini` files contain simple `key=value` pairs. Extract the value corresponding to the requested key.
5. **Reporting**: Create a final report file at `/home/user/recovery_report.txt`. For each rule processed, write a line in the format `filename:extracted_value`. Sort the lines in the report alphabetically.

Ensure the final report strictly contains only the required output.