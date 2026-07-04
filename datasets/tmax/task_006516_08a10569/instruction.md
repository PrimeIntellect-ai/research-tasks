You are a data scientist working on cleaning a batch of messy incoming datasets. The data is currently sitting in a simulated remote staging directory. You need to write a Bash pipeline script to transfer, normalize, and log the processing of this data.

Create a Bash script at `/home/user/process_pipeline.sh` that performs the following steps:

1. **Local-Remote Transfer**: 
   Use `rsync` to sync all `.csv` files from `/opt/staging_server/data/` (the mock remote) to a local working directory `/home/user/raw_data/`. Create the local directory if it doesn't exist.

2. **Pipeline Logging**:
   Throughout the execution, your script must log its progress to `/home/user/pipeline.log`. 
   Every log line must strictly follow this format: `[YYYY-MM-DD HH:MM:SS] <STAGE>: <MESSAGE>`
   - Stage 1: `[YYYY-MM-DD HH:MM:SS] TRANSFER: Successfully synced <N> files.` (where <N> is the number of files transferred).
   - Stage 2: `[YYYY-MM-DD HH:MM:SS] PROCESS: Starting normalization.`
   - Stage 3: `[YYYY-MM-DD HH:MM:SS] COMPLETE: Processed total of <M> valid rows.` (where <M> is the total number of data rows across all files, excluding headers).

3. **Normalization and Standardization**:
   The CSV files contain 4 columns: `id,name,date,country`. 
   Read all the transferred CSV files, skip their header rows, and process the data according to these rules:
   - **id**: Must be a valid integer. If it's empty or non-numeric, drop the row.
   - **name**: Trim leading and trailing whitespaces.
   - **date**: Currently in mixed formats (`MM/DD/YYYY` or `YYYY-MM-DD`). Standardize all dates to `YYYY-MM-DD`. (Assume month and day are always 2 digits, and year is 4 digits).
   - **country**: Trim whitespaces and convert to uppercase (e.g., " us " -> "US", "Uk" -> "UK").

4. **Output**:
   Write the normalized data (with a single header row `id,name,date,country` at the top) to `/home/user/cleaned_master.csv`. The output data rows must be sorted numerically by `id` in ascending order. Fields must be separated by commas without extra spaces around them.

Make sure the script is executable (`chmod +x`) and then execute it so the final output files (`cleaned_master.csv` and `pipeline.log`) are generated.