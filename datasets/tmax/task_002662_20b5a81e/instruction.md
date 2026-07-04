You are tasked with safely recovering and analyzing a series of configuration backups. Our configuration manager tracks changes by periodically backing up JSON configurations into nested archives. Unfortunately, a recent automated backup resulted in a nested archive that contains a potential "Zip Slip" vulnerability (paths attempting to traverse outside the target extraction directory).

Your objective is to safely extract the data, parse the configurations, and generate a change report.

Step 1: Safe Extraction
1. There is a multi-part backup archive located at `/home/user/config_backup.tar.gz`. 
2. Extract the tarball. Inside, you will find several `.zip` files.
3. Write a Python script named `/home/user/safe_extract.py` that iterates through all `.zip` files and extracts their contents into `/home/user/extracted_configs/`.
4. **CRITICAL:** Your Python extraction script MUST prevent "Zip Slip" directory traversal attacks. Any file entry within the zip archives that attempts to extract outside the `/home/user/extracted_configs/` directory (e.g., using `../` or absolute paths) must be completely skipped and NOT extracted anywhere on the file system.
5. Have your script log the skipped malicious paths to `/home/user/skipped_files.log` (one path per line).

Step 2: Configuration Analysis
1. Once safely extracted, you will find JSON configuration files categorized by version (e.g., `v1/config.json`, `v2/config.json`, `v3/config.json`).
2. Write a script to parse these JSON files and compare the configuration state between `v1` and `v3` (ignore `v2`).
3. Identify all keys that exist in BOTH `v1/config.json` and `v3/config.json` but have DIFFERENT values.
4. Output these changed configurations to a CSV file at `/home/user/config_diff.csv`.
5. The CSV must have exactly this header: `Key,V1_Value,V3_Value`
6. The rows must be sorted alphabetically by the `Key` name.

Constraints:
- You may use Bash shell tools and Python 3.
- The system does not have root access, so install any required local tools using `pip` or stay within standard libraries. Python's standard `zipfile` and `json` modules are sufficient.