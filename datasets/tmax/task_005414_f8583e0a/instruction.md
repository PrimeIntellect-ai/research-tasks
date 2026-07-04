You are a storage administrator tasked with managing disk space and consolidating a set of application backups. 

In the `/home/user/backups/` directory, you will find two sets of backups:
1. `base_backup.tar.gz`: A full base backup archive.
2. `incr_backup.tar.gz.part1` and `incr_backup.tar.gz.part2`: A multi-part archive containing an incremental backup.

Your task is to restore these backups and optimize storage by following these precise steps:

1. **Extraction**:
   - Create directories `/home/user/restore/base/` and `/home/user/restore/incr/`.
   - Extract the contents of `base_backup.tar.gz` into the `base/` directory.
   - Recombine the multi-part incremental backup and extract its contents into the `incr/` directory.

2. **Deduplication (Hard Links)**:
   - To save disk space, find all files in the `incr/` directory that have exactly the same content as a file with the same name in the `base/` directory.
   - Replace these duplicate files in the `incr/` directory with **hard links** to the corresponding files in the `base/` directory.

3. **Latest View (Symbolic Links)**:
   - Create a directory `/home/user/restore/latest/`.
   - For every unique filename found across both the `base/` and `incr/` directories, create a **symbolic link** in `/home/user/restore/latest/` pointing to the most up-to-date version of that file. 
   - If a file exists in `incr/`, point the symlink to the `incr/` version (using absolute or relative paths, as long as it correctly resolves). If it only exists in `base/`, point to the `base/` version.

4. **Reporting**:
   - Generate a text file at `/home/user/resolution_report.txt` containing the strictly resolved absolute paths of the target files for all symlinks in `/home/user/restore/latest/`. 
   - The file should contain one absolute path per line, sorted alphabetically by the symlink's file name.

Ensure all directories and links are created exactly as specified.