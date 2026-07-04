You are tasked with creating a robust, atomic file-watching script for an artifact curation system. 

Write a Python script at `/home/user/artifact_watcher.py` that fulfills the following requirements:
1. **Directory Watching**: The script must continuously monitor the directory `/home/user/repo/incoming/` for any new files. You may use a simple polling loop (e.g., checking every 1 second).
2. **Checksum Generation**: Whenever a new file is detected in the `incoming/` directory, calculate its SHA-256 checksum.
3. **Atomic Manifest Update**: Read the existing JSON manifest at `/home/user/repo/manifest.json`. Add the new file's checksum as a key-value pair (`"filename": "sha256_hash"`). Write the updated JSON object back to `manifest.json`. **This write must be atomic.** You must write the updated JSON to a temporary file first, and then atomically replace the original `manifest.json` using standard Python libraries (e.g., `os.replace`).
4. **Curation**: After the manifest is successfully updated, move the processed file to `/home/user/repo/processed/`.
5. **Graceful Shutdown**: If a file exactly named `SHUTDOWN` appears in the `incoming/` directory, the script must exit cleanly (do not process `SHUTDOWN` into the manifest or move it).

After writing the script, perform the following operations in your terminal to test it:
1. Create the directories `/home/user/repo/incoming/` and `/home/user/repo/processed/`.
2. Initialize `/home/user/repo/manifest.json` with an empty JSON object: `{}`
3. Start your Python script in the background.
4. Create three files inside `/home/user/repo/incoming/` with the exact following contents (no trailing newlines):
   - `file1.bin` containing the string: `alpha`
   - `file2.bin` containing the string: `beta`
   - `file3.bin` containing the string: `gamma`
5. Wait a few seconds to ensure they are processed.
6. Create an empty file named `SHUTDOWN` inside `/home/user/repo/incoming/` to stop the background process.

Your task is complete when the script has shut down, `manifest.json` contains the correct checksums, and the three `.bin` files are safely in the `processed/` directory.