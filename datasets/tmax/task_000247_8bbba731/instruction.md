You are a FinOps analyst tasked with optimizing cloud storage costs. The CI/CD pipelines are generating large build artifacts and logs, causing storage costs to balloon. You need to implement an automated storage lifecycle pipeline using Bash that enforces a strict directory size quota by archiving older files. To ensure this new automation doesn't disrupt ongoing CI/CD processes, you must deploy it using a staged pipeline approach.

Your objective is to create two Bash scripts in `/home/user/`: `storage_optimizer.sh` and `run_finops_pipeline.sh`.

**Step 1: Write the Storage Optimizer Script**
Create a robust script at `/home/user/storage_optimizer.sh`.
It must take exactly three arguments:
1. `TARGET_DIR`: The directory to monitor and clean up.
2. `ARCHIVE_DIR`: The directory where older files will be moved.
3. `REPORT_FILE`: The path to a CSV file where the script will append logs of its actions.

The script must perform the following:
- Calculate the total size (in bytes) of all files in `TARGET_DIR`. Do not count subdirectories, only the files directly in `TARGET_DIR`.
- Enforce a "soft quota" of exactly `52428800` bytes (50 MiB).
- If the total size exceeds the quota, the script must identify the oldest files in `TARGET_DIR` (based on modification time) and move them to `ARCHIVE_DIR` one by one until the total size of the files remaining in `TARGET_DIR` is less than or equal to `52428800` bytes.
- For every file moved, append a line to `REPORT_FILE` in the following exact CSV format:
  `timestamp,filename,file_size_bytes,source_dir,dest_dir`
  *(Where `timestamp` is the current Unix epoch time when the move occurred, `filename` is just the base name of the file, `file_size_bytes` is the size of the file in bytes, and directories are absolute paths).*
- Ensure the script handles edge cases gracefully (e.g., creating `ARCHIVE_DIR` if it doesn't exist) and exits with code `0` on success, or non-zero on error.

**Step 2: Construct the Staged CI/CD Pipeline Orchestrator**
Create `/home/user/run_finops_pipeline.sh`. This script will simulate a staged deployment pipeline for your optimizer.
It must:
1. Execute `storage_optimizer.sh` against the staging environment:
   - Target: `/home/user/staging_artifacts`
   - Archive: `/home/user/staging_archive`
   - Report: `/home/user/staging_finops.csv`
2. Check the exit code of the staging run. If it fails, the pipeline must exit immediately with an error code.
3. If the staging run is successful, proceed to the production environment:
   - Target: `/home/user/prod_artifacts`
   - Archive: `/home/user/prod_archive`
   - Report: `/home/user/prod_finops.csv`

**Execution**
Once you have written both scripts, make them executable and run `/home/user/run_finops_pipeline.sh` to perform the automated cleanup.