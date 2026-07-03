You are an AI assistant helping a developer organize and transform legacy project files. 

The developer has a deeply nested archive of old project records located at `/home/user/legacy_assets.tar.gz`. Inside this archive are multiple `.zip` files, and inside those `.zip` files are several `.csv` files containing project data.

Your task consists of several phases spanning extraction, concurrent C programming, and incremental backups.

**Phase 1: Extraction**
1. Extract `/home/user/legacy_assets.tar.gz` into `/home/user/assets_extracted/`.
2. Find and extract all `.zip` files within `/home/user/assets_extracted/` into a directory called `/home/user/csv_data/`.

**Phase 2: Write a Concurrent Transformer in C**
Write a C program at `/home/user/transformer.c` and compile it to `/home/user/transformer`.
The program must:
1. Accept a single file path as a command-line argument (`argv[1]`).
2. Read the specified file, which will be a CSV with the format: `id,project_name,status` (without a header row).
3. Convert each row into a JSON Lines format string: `{"id": "<id>", "project_name": "<project_name>", "status": "<status>"}\n`.
4. Append these JSON strings to a master log file at `/home/user/master_output.json`.
5. **Critical Requirement:** Because this program will be executed concurrently by multiple processes, you **must** use POSIX file locking (`fcntl` or `flock`) to acquire an exclusive write lock on `/home/user/master_output.json` before appending data for a given CSV file, and release it afterward. This prevents interleaving and data corruption.

**Phase 3: Execution via Standard Streams and Piping**
Use a shell pipeline to find all extracted `.csv` files in `/home/user/csv_data/` and pipe them to your compiled C program using `xargs` to ensure concurrent execution. 
Specifically, use `find`, pipe to `xargs -P 4 -n 1 /home/user/transformer` so that 4 processes attempt to write to the master output file simultaneously.

**Phase 4: Incremental Backups**
Once the master JSON file is fully generated:
1. Create a Level 0 (full) incremental backup of `/home/user/master_output.json` using `tar`. Name the archive `/home/user/backup_level0.tar` and use `/home/user/backup.snar` as the snapshot/metadata file.
2. Append a new dummy record to the end of the JSON file: `{"id": "999", "project_name": "final_check", "status": "completed"}`.
3. Create a Level 1 (incremental) backup of `/home/user/master_output.json` using `tar` with the same snapshot file. Name this archive `/home/user/backup_level1.tar`.

Ensure your C code compiles without warnings and handles locks correctly. Do not leave stray lock files or temporary files outside the specified directories.