You are managing a binary artifact repository. You need to automate the curation of incoming build artifacts, saving disk space through deduplication, and preparing differential backups.

Write a Bash script at `/home/user/curate_artifacts.sh` that performs the following operations:

1. **Parse Multi-line Logs**: 
   Read the log file located at `/home/user/incoming/builds.log`. This file contains multi-line build records. Each record begins with `--- BUILD <ID> ---`, contains various log lines, and strictly ends with either `STATUS: SUCCESS` or `STATUS: FAILURE`.
   Identify all `<ID>`s that resulted in a `SUCCESS`.

2. **Extract Archives**:
   For each successful build ID, there is a corresponding uncompressed archive at `/home/user/incoming/archives/build_<ID>.tar`. 
   Extract each successful build's archive into a new directory at `/home/user/curated/build_<ID>/`. Do not extract failed builds.

3. **Space Optimization via Hard Links**:
   Artifacts often contain unchanged binary files (e.g., shared libraries) across different builds. 
   To save space, your script must find all identical regular files within the `/home/user/curated/` hierarchy and replace the duplicates with hard links. 
   *Constraint*: If `fileA` and `fileB` are identical, they must share the same inode. You must write the Bash logic to do this without using external specialized deduplication tools like `fdupes` or `rdfind` (use standard utilities like `find`, `md5sum`, `sort`, `awk`, `ln`, `rm`).

4. **Symlink the Latest Release**:
   Determine the highest numerical `<ID>` among the successful builds.
   Create a symbolic link at `/home/user/curated/latest` that points to the directory `build_<highest_ID>`. (The symlink should point to the target directory name, e.g., `build_105`, not an absolute path).

5. **Create an Incremental Backup**:
   A previous backup state file exists at `/home/user/backup.snar`.
   Using GNU `tar`, create an incremental backup of the `/home/user/curated/` directory at `/home/user/curated_backup.tar.gz`. 
   Use the `--listed-incremental=/home/user/backup.snar` flag. Ensure the archive is gzip compressed.

Make sure your script is executable and run it to produce the final state.

Constraints:
- Do not use root privileges.
- All files and directories must reside in `/home/user/`.
- The final backup must be located exactly at `/home/user/curated_backup.tar.gz`.