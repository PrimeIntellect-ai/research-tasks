You are acting as a backup administrator archiving active database logs and data exports. We have a set of active files in `/home/user/backup_source/` that are actively being written to by production systems. 

Your task is to write a C program and a shell script to safely parse these files, generate a manifest, and archive a subset of them.

Here are the requirements:

**Phase 1: Write a C program (`/home/user/manifest_generator.c`)**
1. The program must recursively traverse the directory `/home/user/backup_source/`.
2. It should look for files with `.csv` and `.wal` extensions.
3. Because these files are actively used, your C program MUST acquire a shared read lock (using `fcntl` POSIX locks) on each file before reading it, and release it afterward.
4. **Parsing `.csv` files:** The CSV files have a header `id,data`. You need to read the file and extract the `id` of the *last* row (assume the ID is an integer).
5. **Parsing `.wal` files:** The WAL files are simple text files. The first line always starts with `TXN_ID: ` followed by an integer. You need to extract this integer.
6. The program must generate a well-formatted JSON file at `/home/user/backup_manifest.json` containing an array of objects. Each object must have `"file_path"` (absolute path) and `"latest_id"` (the extracted integer). The order of the files in the JSON does not matter.

**Phase 2: Compilation and Execution**
Compile your C program into an executable named `/home/user/manifest_generator`. Execute it to generate the `/home/user/backup_manifest.json` file.

**Phase 3: Archiving Script (`/home/user/archive.sh`)**
Write a bash script at `/home/user/archive.sh` that:
1. Creates the directory `/home/user/archive_dest/` if it doesn't exist.
2. Reads `/home/user/backup_manifest.json`. You may install and use `jq` for this.
3. Filters the entries. It should only select files where the `"latest_id"` is **strictly greater than 1000**.
4. Copies the selected files to `/home/user/archive_dest/` (flattening the directory structure, so the files are directly inside `archive_dest`). 

Execute your bash script so the final archived files are in place.