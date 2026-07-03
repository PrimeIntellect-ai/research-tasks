You are tasked with building a configuration management tracker in C that compares configuration states across our server fleet. 

Previously, we used a naive shell script to parse CSV dumps of our server configurations, but it silently dropped or corrupted rows containing embedded newlines (like multiline configuration file contents or SSH keys). We need a robust C program to do this correctly.

Here is your objective:
Write, compile, and execute a C program at `/home/user/config_diff.c` that produces a JSON report of all configuration changes.

**Input Data:**
You will find two directories:
- `/home/user/old_configs/` (contains baseline CSVs)
- `/home/user/new_configs/` (contains updated CSVs)

Each directory contains CSV files named by region (e.g., `us-east.csv`, `eu-west.csv`).
The CSV files are in a "wide" format with the following columns:
`server_id,nginx_config,ssh_keys,env_vars`

**Important CSV constraints:**
- Fields are separated by commas.
- Fields containing commas or newlines are enclosed in double quotes (`"`).
- Double quotes inside quoted fields are escaped as `""`.
- You MUST correctly handle embedded newlines within quoted fields without dropping the row.

**Program Requirements:**
1. **Parallel Processing:** Use `pthreads` to process multiple CSV files concurrently. Spawn at least one thread per region file to perform the parsing and comparison.
2. **Wide-to-Long Reshaping & Merging:** For each server, reshape the wide columns (`nginx_config`, `ssh_keys`, `env_vars`) into key-value pairs. Merge the data from `old_configs` and `new_configs` by matching `server_id` and the field key.
3. **Change Detection:** If the string value of a field has changed between the old and new configurations, record it.
4. **Template-Based Output:** Generate a valid JSON report at `/home/user/diff_report.json` based on the detected changes. You must write the JSON serialization yourself using template formatting in C.

**Output Format (`/home/user/diff_report.json`):**
The output must be a strict JSON array of objects, sorted alphabetically by `server_id`. Each object should list the fields that changed, sorted alphabetically by field name.

Example format:
```json
[
  {
    "server_id": "srv-101",
    "changes": [
      {
        "field": "nginx_config",
        "old_length": 45,
        "new_length": 48
      },
      {
        "field": "ssh_keys",
        "old_length": 200,
        "new_length": 200
      }
    ]
  }
]
```
Note: If a server has no changes, omit it from the JSON array entirely. The length refers to the byte length of the unquoted string (e.g., "A\nB" is length 3).

Write your code, compile it (e.g., using `gcc -pthread -o config_diff config_diff.c`), run it, and ensure `/home/user/diff_report.json` is generated successfully.