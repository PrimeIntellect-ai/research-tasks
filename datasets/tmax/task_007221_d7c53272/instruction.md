You are acting as a backup administrator archiving image data. Your task is to write and execute a Python script at `/home/user/run_backup.py` that performs a smart, incremental backup of PNG files based on a configuration file.

Here are the exact requirements for your script:

1. **Configuration Interpretation:** The script must read an INI configuration file located at `/home/user/backup.ini`. This file has a `[Backup]` section with three keys: `source_dir`, `archive_path`, and `state_file`.
2. **Binary Header Extraction:** The script must iterate through all files in the directory specified by `source_dir`. It should only consider files that are valid PNG files. A file is considered a valid PNG *only* if its first 8 bytes match the PNG magic number: `\x89PNG\r\n\x1a\n`. Ignore file extensions completely.
3. **Incremental Backup:** The script must read the JSON state file specified by `state_file` (if it exists). This file contains a dictionary mapping filenames (just the basename, e.g., "image.png") to their last modification time (as a float). The script should only select valid PNG files that are either NOT in the state file, or have a modification time strictly greater than the time recorded in the state file.
4. **Archive Creation:** The script must pack the selected files into a new gzipped tarball (`.tar.gz`) at the path specified by `archive_path`. The files inside the tarball should not include absolute paths (store them at the root of the archive or relative to the source dir).
5. **Atomic Writes:** After successfully creating the archive, the script must update the state file to reflect the current modification times of *all* valid PNG files currently in the directory (not just the ones backed up this time). This update must be done atomically: write the new JSON data to a temporary file first, then atomically replace the old state file with the new one.

Once you have written the script, execute it to perform the backup.