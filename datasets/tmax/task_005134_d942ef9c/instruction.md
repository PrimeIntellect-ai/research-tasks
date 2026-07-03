You are an artifact manager for a binary repository. Your organization receives nested artifact packages and needs an automated pipeline to process, convert, and safely publish them.

Your task is to create a Python script that watches a directory for new artifact bundles, extracts the nested contents, converts metadata formats, and atomically publishes the curated files to a production directory.

Write a Python script at `/home/user/curator.py` that does the following:
1. Uses a directory-watching mechanism (you may install the `watchdog` library via pip, or use simple polling) to monitor the `/home/user/incoming/` directory for new `.zip` files.
2. When a `.zip` file is detected (e.g., `release_1.zip`):
   - It extracts the zip file. Inside you will find an `inner.tar.gz` and a `signature.bin`.
   - It extracts `inner.tar.gz`. Inside you will find `binary.elf` and `metadata.ini`.
   - It converts the `metadata.ini` file into a `metadata.json` file. The JSON file must represent the INI sections and key-value pairs exactly (e.g., `{"section": {"key": "value"}}`).
3. It packages/arranges the final curated artifacts (`binary.elf`, `signature.bin`, and `metadata.json`) and publishes them to `/home/user/published/<original_zip_name_without_ext>_curated/` (e.g., `release_1_curated`).
4. **Atomic publishing requirement:** To prevent partial reads by downstream systems, the script *must* construct the final directory inside a temporary location first, and then use an atomic rename/move operation (`os.rename` or `shutil.move` onto the same filesystem) to place the directory in `/home/user/published/`.

After writing your script:
1. Start your script in the background.
2. Manually trigger the pipeline by copying the prepared bundle from `/home/user/hold/release_1.zip` into `/home/user/incoming/`.
3. Wait for the processing to finish, then copy the generated `metadata.json` from the published directory to `/home/user/success.log` to prove completion.

Ensure you install any required Python packages (like `watchdog`) before running your script.