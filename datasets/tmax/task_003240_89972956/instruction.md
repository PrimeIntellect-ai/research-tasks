I am a data scientist working on a new project and I need to build a reproducible Bash pipeline to clean some raw sensor datasets. 

I have a set of raw CSV files located in `/home/user/raw_data/`. Each file contains sensor readings with the following headers:
`timestamp,sensor_id,temperature,humidity,status`

Unfortunately, the data contains errors. I need you to write a Bash script at `/home/user/clean_pipeline.sh` that processes all `.csv` files in the `/home/user/raw_data/` directory and saves the cleaned versions to `/home/user/clean_data/` (maintaining the original filenames).

The pipeline must perform the following operations using standard Linux tools (like `awk`, `grep`, `cut`, etc.):
1. Create the `/home/user/clean_data/` directory if it doesn't already exist.
2. For each CSV file, keep the header row.
3. Remove any data row where the `status` column is exactly the string `ERROR`.
4. Remove any data row where the `temperature` column is exactly `999.9` (which indicates a sensor malfunction).
5. Extract and keep only the first three columns: `timestamp,sensor_id,temperature`.
6. The output should be a valid, comma-separated file.

To prove that the pipeline is reproducible and deterministic, once your script has processed the files, generate SHA-256 checksums of all the cleaned CSV files in the `/home/user/clean_data/` directory. Save these checksums to a file at `/home/user/checksums.txt` using the standard `sha256sum` command output format (e.g., `sha256sum /home/user/clean_data/*.csv > /home/user/checksums.txt`).

Please write the script, execute it, and generate the required checksum file.