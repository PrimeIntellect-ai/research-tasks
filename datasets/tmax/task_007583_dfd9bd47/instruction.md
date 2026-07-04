You are assisting a machine learning researcher in managing a large, evolving image dataset. To save disk space while maintaining multiple versions of the dataset, we need to implement a hard-link-based snapshot system and generate incremental backup archives.

Currently, the active dataset is located in `/home/user/raw_data`. 
A previous snapshot of this dataset exists at `/home/user/snapshots/v1`. 
Since `v1` was taken, files in `/home/user/raw_data` have been added, modified, or deleted.

Your task is to:

1. Write a Python script at `/home/user/create_snapshot.py` that takes three arguments: `<source_dir> <dest_dir> <prev_snapshot_dir>`.
   - The script must synchronize the `<dest_dir>` to perfectly match the contents of `<source_dir>`.
   - To save space, if a file exists in both `<source_dir>` and `<prev_snapshot_dir>` and has the exact same content (you can assume files with the same name, size, and modification time are identical), it MUST be hard-linked from `<prev_snapshot_dir>` into `<dest_dir>`.
   - If a file is new or modified, it must be copied as a standard file into `<dest_dir>`.
   - Files deleted from `<source_dir>` should not appear in `<dest_dir>`.

2. Execute your script to create a new snapshot at `/home/user/snapshots/v2` using `/home/user/raw_data` as the source and `/home/user/snapshots/v1` as the previous snapshot.

3. Create an incremental backup archive named `/home/user/patch_v1_to_v2.tar.gz`. This archive must be a gzip-compressed tarball containing ONLY the files that are new or have been modified in `v2` compared to `v1`. The paths in the archive should be relative to the `/home/user/snapshots/v2` directory (e.g., extracting it should yield `data_001.csv`, not `home/user/snapshots/v2/data_001.csv`).

4. Create a plain text report at `/home/user/report.txt` with exactly the following three lines, replacing the bracketed values with the correct integers based on the `v2` snapshot generation:
   New files: [X]
   Modified files: [Y]
   Unmodified files: [Z]

Note: You can use any standard Linux commands and Python 3 standard libraries. Ensure file modification times are preserved when copying so future comparisons work correctly.