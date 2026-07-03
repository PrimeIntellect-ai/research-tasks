You are acting as a storage administrator to manage and optimize disk space on a Linux server. A local application generates significant amounts of data, and we are running low on disk space. We suspect there are duplicate files taking up space, but we cannot safely touch files that are currently marked as "ACTIVE" by the application.

Your objective is to write a Python script at `/home/user/storage_manager.py` that reads the system's configuration, parses the application's multi-line log to determine file status, performs deduplication using hard links, and archives inactive files using symbolic links.

Here are the specific requirements:

1. Read the configuration file `/home/user/storage_conf.ini`. It has the following structure:
   - Under `[Paths]`:
     - `TargetDir`: The directory containing the data files.
     - `LogFile`: The path to the application's multi-line log.
     - `ArchiveLinksDir`: The directory where archive symbolic links should be placed.
   - Under `[Settings]`:
     - `Deduplicate`: A boolean indicating if deduplication should run.
     - `CreateArchiveLinks`: A boolean indicating if archive symlinks should be created.

2. Parse the multi-line log file specified in `LogFile`. The log consists of multi-line records separated by a blank line. A single record looks like this:
   ```
   [YYYY-MM-DD HH:MM:SS] INFO - Job Start
   Job ID: <number>
   File: <full_file_path>
   Status: <ACTIVE|INACTIVE>
   ```
   A file is considered "INACTIVE" only if its *most recent* log entry in the file has the status `INACTIVE`. If a file has no entries, do not process it.

3. If `Deduplicate` is true, find all "INACTIVE" files in `TargetDir` that are exact duplicates of each other (identical file content). For each set of duplicates, keep the file that appears first alphabetically by its base name, and replace all other duplicate files in the set with a **hard link** to that first file. Do not touch "ACTIVE" files.

4. If `CreateArchiveLinks` is true, create a **symbolic link** in the `ArchiveLinksDir` for every "INACTIVE" file found in `TargetDir` (even if it was deduplicated). The symlink should have the same base name as the target file and should point to its absolute path. If `ArchiveLinksDir` does not exist, create it.

5. After executing the operations, your Python script must output a JSON file at `/home/user/summary.json` containing exactly the following keys:
   - `"bytes_saved"`: An integer representing the total size in bytes of the duplicate files that were removed and replaced by hard links (i.e., if you replace a 10-byte file with a hardlink to another file, you saved 10 bytes).
   - `"hard_links_created"`: An integer representing the number of hard links created during deduplication.
   - `"symlinks_created"`: An integer representing the number of symbolic links created in the archive directory.

Write the Python script, run it, and ensure `/home/user/summary.json` is generated correctly.