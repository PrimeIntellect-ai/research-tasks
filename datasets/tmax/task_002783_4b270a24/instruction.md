You are tasked with organizing a chaotic data processing project and setting up its automated pipeline. The project is located at `/home/user/data_project`.

Phase 1: Data Organization & Schema Migration (Python)
The directory `/home/user/data_project/raw` contains several JSON files with an outdated schema (V1). You need to write a Python script at `/home/user/data_project/migrate.py` that reads all `.json` files in the input directory, upgrades them to Schema V2, and organizes them into a new directory structure.

Schema V1 format:
```json
{
  "record_id": "X99",
  "user_name": "Jane Doe",
  "epoch_time": 1641042000
}
```

Schema V2 format requirement:
```json
{
  "record_id": "X99",
  "first_name": "Jane",
  "last_name": "Doe",
  "year": 2022
}
```
*Note: `year` should be extracted from the `epoch_time` (UTC).*

The Python script must accept exactly two command-line arguments: the input directory and the output directory.
Example: `python3 migrate.py /home/user/data_project/raw /home/user/data_project/processed`

The script must save the migrated files in the output directory, organized by year, using the `record_id` as the filename: `<output_dir>/<year>/<record_id>.json`.

Phase 2: CI/CD Pipeline & Conditional Build Setup (Bash)
We need to automate this process. Write a bash script at `/home/user/data_project/setup_ci.sh` that, when executed, generates a GitHub Actions workflow file at `/home/user/data_project/.github/workflows/pipeline.yml`.

The generated `pipeline.yml` must include:
1. A job named `process-data` that runs on `ubuntu-latest`.
2. A step that executes your `migrate.py` script, migrating data from `raw/` to `processed/`.
3. A conditional build step named `cross-compile-tools` that simulates cross-compiling a helper tool for `arm64`. It should contain the exact command: `make build ARCH=arm64`.

Ensure `/home/user/data_project/setup_ci.sh` is executable. You do not need to create the actual `make` build files; just generating the YAML pipeline and writing the Python script is sufficient. 

Please proceed to create `migrate.py` and `setup_ci.sh` fulfilling all the requirements.