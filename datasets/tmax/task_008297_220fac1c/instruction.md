You are an infrastructure engineer automating the provisioning of a storage maintenance service for a data-ingestion pipeline. You need to deploy a Python-based "janitor" script that monitors disk usage and archives processed files using text-processing shell utilities.

Complete the following tasks in the `/home/user` directory.

Phase 1: Environment Setup
1. Create a shell profile file at `/home/user/.deploy_rc`.
2. In this file, export the following environment variables:
   - `JANITOR_DATA_DIR=/home/user/data`
   - `JANITOR_ARCHIVE_DIR=/home/user/archive`
   - `JANITOR_QUOTA_KB=1500`
3. Create the `/home/user/archive` directory. (The `/home/user/data` directory and its contents have already been provisioned by another system).

Phase 2: Text Processing & Monitoring Script
1. Write a robust Python script at `/home/user/storage_janitor.py`.
2. The script must read the environment variables defined above. (Assume the script will be run in an environment where `.deploy_rc` has been sourced).
3. The script must calculate the total size of all files in `JANITOR_DATA_DIR` in kilobytes. (Calculate this as the sum of bytes of all files, divided by 1024).
4. If the total size strictly exceeds `JANITOR_QUOTA_KB`, the script must identify which files are safe to archive. 
   - Inside `JANITOR_DATA_DIR`, there is a file named `manifest.txt`. Each line contains a filename and its status (e.g., `file1.txt STATUS=PROCESSED`).
   - Your Python script **must** use a shell pipeline involving `grep` and `awk` via the `subprocess` module to extract just the filenames of files that have the status `STATUS=PROCESSED`.
5. For each processed file identified by the pipeline, move it from `JANITOR_DATA_DIR` to `JANITOR_ARCHIVE_DIR`.
6. Finally, the script must output a JSON summary file at `/home/user/janitor_report.json` with the exact following schema:
   ```json
   {
     "initial_size_kb": <float, total size before archiving>,
     "quota_exceeded": <boolean>,
     "files_archived": [<list of strings, filenames moved>],
     "final_size_kb": <float, total size after archiving>
   }
   ```

Phase 3: Execution
Run your script. To do this, source your `.deploy_rc` file and execute `python3 /home/user/storage_janitor.py` in the terminal to perform the maintenance run and generate the `janitor_report.json`.