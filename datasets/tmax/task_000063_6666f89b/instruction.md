You are tasked with creating a specialized backup tool for our staging servers. You must write a Python script that traverses a target directory, filters files based on a configuration, and packs them into a custom continuous binary archive format, all while avoiding infinite symlink loops. 

Additionally, you need to use a specific vendored library for directory traversal and synchronization that we have stored locally, but it seems to have a bug regarding symlink handling that you must patch first.

Requirements:
1. **Vendored Package Patching**: We have vendored the `dirsync` package at `/app/dirsync-2.2.5`. However, there is a deliberate perturbation in `dirsync/sync.py` where symlink loop detection was accidentally removed, causing it to crash or hang on circular symlinks. You must fix this perturbation so the package correctly skips infinite symlink loops without throwing exceptions, then install it in your environment.
2. **Configuration File Interpretation**: Your script must read a configuration file located at `/home/user/backup_config.json` inside the target directory. This JSON file contains a key `exclude_extensions` (a list of string extensions like `[".tmp", ".log"]`) and `min_mtime` (an integer timestamp).
3. **Directory Traversal & Search**: Use the fixed `dirsync` library (or your own safe traversal logic complementing it) to recursively find all files in the target directory (passed as the first CLI argument) that do NOT have the excluded extensions and have an `mtime` strictly greater than `min_mtime`. 
4. **Custom Binary Archive**: Your Python script (`/home/user/archiver.py`) must write the matching files into a single binary archive file (passed as the second CLI argument).
    - The format must be exactly as follows for each file, sequentially:
        - 2 bytes: length of the relative file path (unsigned short, big-endian)
        - N bytes: the relative file path string (UTF-8)
        - 8 bytes: file modification time (unsigned long long, big-endian)
        - 4 bytes: file size in bytes (unsigned int, big-endian)
        - M bytes: the actual raw binary contents of the file.
    - Files must be processed and appended to the archive in strict alphabetical order of their relative paths.

Ensure your script `/home/user/archiver.py` takes exactly two arguments:
`python3 /home/user/archiver.py <target_directory> <output_archive_path>`