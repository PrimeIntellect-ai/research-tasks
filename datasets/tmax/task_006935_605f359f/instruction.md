You are an artifact manager responsible for curating binary repositories. Your system performs incremental backups of large binary assets stored across various storage volumes. 

Currently, your backup system is broken, and you need to manually perform an incremental backup based on a messy manifest file, using shell tools and a custom C program.

Here is the current state of your system:
- Old backup manifest: `/home/user/old_manifest.csv` (Format: `ArtifactID,ResolvedAbsolutePath,Version`)
- Messy new manifest: `/home/user/raw_new_manifest.txt` (Contains messy, inconsistent paths and spacing)
- Actual binary artifacts are stored in `/home/user/storage/vol1/` and `/home/user/storage/vol2/`.

Your task involves three steps:

**Step 1: Text Transformation**
The file `/home/user/raw_new_manifest.txt` is poorly formatted. It contains extraneous spaces, uses backslashes (`\`) instead of forward slashes (`/`), and has relative paths (e.g., `./storage/vol1/...` or `storage/vol2/...`) instead of absolute paths. 
Using tools like `sed` or `awk`, clean this file and save it to `/home/user/clean_new_manifest.csv`. 
The clean file must strictly follow the format: `ArtifactID,ResolvedAbsolutePath,Version` (no spaces around commas, absolute paths starting with `/home/user/`).

**Step 2: Differential Logic in C**
Write a C program at `/home/user/backup_manager.c` and compile it to `/home/user/backup_manager`.
This program must:
1. Read `/home/user/old_manifest.csv` and `/home/user/clean_new_manifest.csv`.
2. Identify which artifacts are "new" (ArtifactID does not exist in the old manifest) or "updated" (Version in the new manifest is strictly greater than the Version in the old manifest).
3. Copy only these new or updated binary files from their respective storage volumes into the directory `/home/user/incremental_backup/`. (Create this directory if it doesn't exist).
4. Preserve the original file names when copying.

**Step 3: Logging**
As your C program copies the files, it must write a log file to `/home/user/backup_log.txt`. 
The log file must contain the exact absolute paths of the files that were backed up, one per line, sorted alphabetically.

Complete the cleanup, write and run your C code, and ensure the incremental backup is successfully created in `/home/user/incremental_backup/` along with the accurate `/home/user/backup_log.txt`.