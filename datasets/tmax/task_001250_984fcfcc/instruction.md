You are an AI assistant helping a researcher organize their messy datasets into a clean, standardized directory structure. To save disk space, the researcher wants to use hard links wherever possible, but some files need format conversion first.

You need to write and execute a Bash script at `/home/user/organize.sh` that reads a pipeline configuration file and performs the organization.

The configuration file is located at `/home/user/dataset_pipeline.conf`. It is a pipe-separated (`|`) text file with the following columns:
`source_file | target_directory | target_filename | target_format | is_latest`

Your script `/home/user/organize.sh` must do the following for each line in the config file (skipping empty lines or lines starting with `#`):
1. Parse the line to extract the fields.
2. Create the `target_directory` if it doesn't already exist.
3. Check if the `source_file` needs format conversion based on its current extension and the requested `target_format`.
    * If the source is `.json` and the target format is `csv`, convert the JSON file (an array of flat objects) into a standard CSV format (with a header row matching the JSON keys) and save it as `target_directory/target_filename`. You must use standard Linux tools (like `jq`) for this.
    * If the source file already matches the `target_format` (e.g., a `.csv` going to a `csv`), **do not copy the file**. Instead, create a **hard link** from the `source_file` to `target_directory/target_filename` to save disk space. If the target file already exists, overwrite it.
4. If the `is_latest` column is set to `true`, create a **symbolic link** at `/home/user/clean_data/latest_dataset` that points to the `target_directory` of that dataset. If a symlink already exists there, update it to point to the new directory.

Before you begin, create the following setup files to test your script:
1. `/home/user/raw_data/alpha.json`:
```json
[
  {"timestamp": 1620000000, "sensor": "A", "reading": 45.2},
  {"timestamp": 1620000060, "sensor": "A", "reading": 46.1}
]
```
2. `/home/user/raw_data/beta.csv`:
```csv
timestamp,sensor,reading
1620000120,B,42.8
1620000180,B,43.0
```
3. `/home/user/dataset_pipeline.conf`:
```text
# Pipeline Configuration
/home/user/raw_data/alpha.json|/home/user/clean_data/alpha_exp|results.csv|csv|true
/home/user/raw_data/beta.csv|/home/user/clean_data/beta_exp|results.csv|csv|false
```

Write the script, ensure it is executable, and then execute it so the final directory structure is created. Ensure the script works generically for any similar config file, not just the test data.