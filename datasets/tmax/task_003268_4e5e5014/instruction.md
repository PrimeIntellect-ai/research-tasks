You are acting as a configuration manager. We have a series of backup archives containing system configurations from different points in time, but the formats are inconsistent and changes have not been tracked. 

Your task is to standardize the configuration formats, track the changes between the oldest and newest backups, and package the latest configuration into a clean archive.

Here is your starting point:
In `/home/user/backups/`, you will find three archives:
- `v1.tar.gz`
- `v2.zip`
- `v3.tar.gz`

Please perform the following steps:
1. Extract all three archives into `/home/user/extracted/v1`, `/home/user/extracted/v2`, and `/home/user/extracted/v3` respectively.
2. Write a Python script (e.g., `/home/user/process.py`) to recursively process the extracted directories. 
3. For EVERY version, convert all `.ini` files into `.json` files and then delete the original `.ini` files. 
   - The JSON structure should mirror the INI structure: a top-level object containing section names as keys, which map to objects containing the key-value pairs (e.g., `{"section_name": {"key_name": "value"}}`). 
   - Use Python's standard `configparser` and `json` libraries. Treat all parsed INI values as strings.
4. Compare the configurations in `/home/user/extracted/v1` against `/home/user/extracted/v3`. 
   - Create a file at `/home/user/report.json` that catalogs the differences. 
   - The report must be a JSON object with two keys: `"changed"` and `"new"`.
   - `"changed"`: A sorted list of relative file paths (e.g., `"system/network.json"`) that exist in both versions but have different file contents (string inequality of the formatted JSON, or dictionary inequality, both are fine as long as the data changed).
   - `"new"`: A sorted list of relative file paths that exist in `v3` but not in `v1`.
5. Create a final, consolidated archive at `/home/user/latest_config.tar.gz`. 
   - This archive must contain the contents of the `/home/user/extracted/v3/` directory at its root (e.g., extracting the tarball should yield `system/` and `app/` directly, not nested inside a `v3/` directory).
   - It must also contain your `report.json` at the root of the archive.

Ensure your Python script runs cleanly and all outputs exactly match the specified structures.