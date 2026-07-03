You are an AI assistant helping a data researcher organize and back up a continuous stream of dataset files.

The researcher has a live dataset directory at `/home/user/live_dataset` which is constantly being written to. A previous full backup exists at `/home/user/backups/full_backup.tar.gz`.

To avoid race conditions with the writing process without stopping it, you need to create a snapshot using hard links, perform a differential backup of only the new or changed files, and verify the backup archive.

Please perform the following steps using Bash commands:
1. Create a directory named `/home/user/dataset_snapshot`.
2. Create hard links for all files currently in `/home/user/live_dataset` inside `/home/user/dataset_snapshot`. Keep the same filenames. (Assume a flat directory structure with no subdirectories).
3. Identify which files in `/home/user/dataset_snapshot` are newer than the file `/home/user/backups/full_backup.tar.gz`.
4. Create a compressed tar archive named `/home/user/backups/inc_backup.tar.gz` that contains ONLY these newer files. The paths in the archive must be exactly the relative filenames (e.g., `data3.csv`), without the absolute directory path.
5. Verify the integrity of your new archive by listing its contents using `tar` and redirecting the sorted output to `/home/user/backups/verify.log`.

Ensure all operations are completed in `/home/user` and the final `verify.log` contains only the exact filenames of the incrementally backed up files, sorted alphabetically, one per line.