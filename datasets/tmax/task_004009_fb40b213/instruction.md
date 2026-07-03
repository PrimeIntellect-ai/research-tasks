You are acting as a backup administrator for a critical application. The previous administrator left behind a broken backup pipeline that fails due to circular symlinks and lacks proper data sanitization. Your task is to fix the pipeline, sanitize the data, extract specific log events, and generate a final backup archive.

All work should be done in `/home/user/`.
The source data is located in `/home/user/data_to_backup/`.

Here are your specific objectives:

1. **Fix the Infinite Symlink Loop:**
   There is a Python script at `/home/user/backup_generator.py` intended to traverse the `/home/user/data_to_backup/` directory and collect files to archive. However, it currently gets stuck in an infinite loop due to circular symlinks left in the directory structure. 
   Modify `/home/user/backup_generator.py` so that it safely traverses the directory structure. It must skip *all* symlinks entirely (do not include symlinks or their targets in the final list of files to backup). 

2. **Text Transformation & Data Sanitization:**
   The file `/home/user/data_to_backup/config.xml` contains sensitive IPv4 addresses. Before archiving, you must redact all IPv4 addresses in this file, replacing them with the exact string `XXX.XXX.XXX.XXX`. Modify the file in-place or ensure the version that gets backed up is redacted.

3. **Multi-line Log Parsing:**
   The file `/home/user/data_to_backup/app.log` contains multi-line log entries. You must write a Python script (or add to `backup_generator.py`) to parse this file and extract all `ERROR` level logs, which span multiple lines due to stack traces.
   Save the extracted errors to `/home/user/extracted_errors.json` in the following format:
   ```json
   [
     {
       "timestamp": "YYYY-MM-DD HH:MM:SS",
       "level": "ERROR",
       "message": "The main error message",
       "traceback": "The full multi-line stack trace... (including the leading tabs/spaces)"
     }
   ]
   ```
   A log entry starts with `[YYYY-MM-DD HH:MM:SS] LEVEL - Message`. Any subsequent lines before the next `[` belong to the `traceback` of the current entry.

4. **Final Archive Generation:**
   Once the above steps are complete, execute your fixed `/home/user/backup_generator.py` to produce `/home/user/backup.tar.gz`. 
   The archive should contain the contents of `/home/user/data_to_backup/` (with the redacted `config.xml`), but must *exclude* any symlinks, and must *exclude* any files larger than 5 MB (metadata-based exclusion). The paths inside the tarball should be relative to `/home/user/data_to_backup/` (e.g., `app.log`, `config.xml`).

Ensure your final JSON is valid and accurately captures the multi-line traces, the XML is correctly redacted without breaking its structure, and the `.tar.gz` is successfully created without infinite loop crashes.