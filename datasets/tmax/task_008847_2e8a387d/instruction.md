You are an AI assistant helping a developer organize their project files securely. 

We have a system that receives automated project updates via ZIP archives. Recently, we discovered that some archives contain potentially malicious paths (Zip Slip vulnerability). You need to write a Python script that securely processes these archives, performs an incremental backup of the files, and updates a state file safely.

Write a Python script at `/home/user/organize.py` that does the following:

1. **Configuration Interpretation:**
   Read a JSON configuration file located at `/home/user/config.json`. It contains the following keys:
   - `incoming_dir`: The directory containing ZIP files to process.
   - `backup_dir`: The directory where files should be permanently stored.
   - `state_file`: The path to the JSON file tracking the current backup state.

2. **File Locking:**
   Before processing, the script must acquire an exclusive lock on a file named `backup.lock` in the `/home/user/` directory using `fcntl.flock` (with `fcntl.LOCK_EX | fcntl.LOCK_NB`). If it cannot acquire the lock, it should exit immediately with code 1. Keep the lock until the script finishes.

3. **Secure Extraction (Zip Slip Prevention):**
   Find all `.zip` files in the `incoming_dir`. For each archive:
   - Iterate through its members.
   - If a member's path is absolute or resolves to a location outside the intended extraction target (e.g., contains `../` trying to escape the root of the archive), **do not extract it**. 
   - Append the exact original path of any skipped malicious member to `/home/user/skipped.log` (one path per line).
   - Extract the safe files to a temporary staging directory (e.g., using `tempfile.TemporaryDirectory`).

4. **Incremental Backup:**
   For each safe file extracted into the staging area:
   - Calculate its MD5 hash.
   - Check if the file already exists in `backup_dir` at the same relative path.
   - Only copy the file from the staging area to the `backup_dir` if it does not exist there, or if its MD5 hash differs from the one currently recorded in the `state_file`.
   - Ensure missing subdirectories in `backup_dir` are created as needed.

5. **Atomic State Update:**
   The `state_file` keeps track of the backup state. It is a JSON file mapping relative file paths (e.g., `src/main.py`) to their MD5 hashes.
   - After processing all archives, update the state dictionary with any new or modified files.
   - Write the new state dictionary to disk **atomically**. Write to a temporary file in the same directory (e.g., `state.json.tmp`), ensure all data is flushed to disk (`f.flush()`, `os.fsync()`), and then use `os.replace()` to overwrite the original `state_file`.

**Execution:**
Once you have written `/home/user/organize.py`, execute it to process the existing files in `/home/user/incoming/`.

Constraints:
- Only use standard Python libraries (no `pip install` required).
- The final state file must be strictly formatted JSON.