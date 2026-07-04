You are tasked with building a configuration manager that tracks state changes from Write-Ahead Logs (WAL) and consolidates them into a minified JSON configuration file. 

You have been provided an image at `/app/schema_info.png` that contains the schema definition for our configurations. It lists the `ALLOWED_KEYS` that are permitted in the final configuration.

The WAL files are stored in `/home/user/wal_logs/` as chunked files (`chunk_01.log`, `chunk_02.log`, etc.). Each line in these logs represents a state change:
- `SET <key> <value>` sets or updates a key.
- `DELETE <key>` removes a key.

Your objective is to:
1. Extract the `ALLOWED_KEYS` from the image `/app/schema_info.png` using OCR (e.g., `tesseract`).
2. Write a Bash script `/home/user/consolidate.sh` that processes the WAL chunks in alphabetical order.
3. The script must reconstruct the final configuration state by applying the operations in sequence.
4. Filter the final state to ONLY include keys that are present in the `ALLOWED_KEYS` extracted from the image. Keys that were deleted or are not in the allowed list must not appear in the final output.
5. The script must output the final state as a strictly minified JSON object (no spaces, no newlines) to `/home/user/output/latest_config.json`.
6. You must use atomic writes for the final output (e.g., write to a hidden temporary file in the same directory, then move it to the final destination).
7. Create a symbolic link at `/home/user/current_config` that points to `/home/user/output/latest_config.json`.

Make sure the final JSON file is as small as possible. The automated test will measure the file size of your JSON output to ensure it is minified correctly, and will verify that the JSON structure perfectly matches the expected configuration state.