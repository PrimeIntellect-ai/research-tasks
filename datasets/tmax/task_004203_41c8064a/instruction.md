I need you to help me organize some scattered project assets by writing and executing a Python script. I have a nested archive containing various logs and source files, and I need to clean up the logs and generate a secure manifest of the final files.

Please create and run a Python script at `/home/user/process_assets.py` that performs the following steps:

1. **Extract Nested Archives**: I have an archive located at `/home/user/project_data.tar.gz`. Extract it into `/home/user/extracted/`. Inside, you will find several `.zip` files. Extract all of these `.zip` files into directories matching their base name (e.g., `module1.zip` should be extracted into `/home/user/extracted/module1/`). You can delete the `.zip` files after extracting them.

2. **Text Transformation**: Find all `.log` files within the extracted directories (e.g., `/home/user/extracted/module1/app.log`). Modify these files in-place with the following rules:
   - Remove any line that contains the exact string `DEBUG` (case-sensitive).
   - Replace any occurrence of the exact string `WARN` with `WARNING` (case-sensitive).

3. **Manifest Generation and Atomic Write**: Compute the SHA-256 checksum for every file inside `/home/user/extracted/` (including all subdirectories, but excluding directories themselves). 
   - Create a JSON object where the keys are the file paths *relative* to `/home/user/extracted/` (e.g., `module1/app.log`) and the values are their lowercase hex SHA-256 hashes.
   - Write this JSON object to a file. To prevent data corruption in case of a crash, you **must** use an atomic write pattern: write the JSON data to a temporary file at `/home/user/final_manifest.json.tmp` first, ensure it is fully written, and then atomically rename it to `/home/user/final_manifest.json`.

Ensure your script is self-contained and runs without errors. Leave the final `/home/user/final_manifest.json` and `/home/user/extracted/` directory in place for verification.