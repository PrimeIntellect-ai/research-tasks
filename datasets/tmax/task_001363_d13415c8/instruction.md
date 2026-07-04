You are a backup administrator tasked with modernizing and archiving legacy data dumps.

You have been provided with a compressed archive located at `/home/user/legacy_data.tar.gz`. This archive contains two files exported from old systems with different formats and character encodings:
1. `hr_data.csv` - A comma-separated values file encoded in Windows-1252. The header is `id,name,role`. It contains names with special accented characters.
2. `finance_data.json` - A JSON file containing an array of objects, encoded in UTF-16. 

Your task is to perform the following operations:
1. **Extraction**: Extract the contents of `/home/user/legacy_data.tar.gz`.
2. **Transformation & Encoding Conversion**: Write and execute a Python script to read these files using their correct legacy encodings and convert them both to UTF-8 encoded JSON Lines (JSONL) format. 
   - The output files should be named `hr_data.jsonl` and `finance_data.jsonl` and must be saved in a new directory: `/home/user/normalized/`.
   - Each line in `hr_data.jsonl` should be a JSON object representing a row from the CSV (keys: `id`, `name`, `role`).
   - Each line in `finance_data.jsonl` should be a JSON object representing an item from the original JSON array.
3. **Manifest Creation**: Create a manifest file at `/home/user/normalized/manifest.json`. This must be a single JSON object where the keys are the original filenames (`hr_data.csv`, `finance_data.json`) and the values are the integer counts of the number of records (lines) processed for each file.
4. **Archiving**: Compress the entire `/home/user/normalized/` directory into a new zip archive located at `/home/user/final/backup_v2.zip`. (Create the `/home/user/final/` directory if it does not exist).
5. **Service**: To simulate making this archive available to the ingestion service, start a Python HTTP server in the background that serves the `/home/user/final/` directory on port `8123`. 
6. Save the Process ID (PID) of this background HTTP server into a file at `/home/user/server.pid`.

Ensure all output files use strictly UTF-8 encoding.