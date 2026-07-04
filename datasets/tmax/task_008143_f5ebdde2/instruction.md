You are an artifact manager maintaining a local binary repository. We have received a new batch of hashed binaries that need to be semantically renamed and added to an incremental backup.

Your workspace is located at `/home/user/repo`.

Inside, you will find:
1. `/home/user/repo/binaries/` - A directory containing newly downloaded binary files with hashed filenames (e.g., `a1b2c3.bin`).
2. `/home/user/repo/mapping.csv` - A CSV file mapping the hashed names to semantic version names. Format: `hashed_name,semantic_name` (e.g., `a1b2c3.bin,app-v1.0.0.bin`).
3. `/home/user/repo/staging/` - An empty staging directory.
4. `/home/user/backup/` - Contains a snapshot file `snapshot.snar` used for incremental backups.

Perform the following operations:
1. Copy all binaries from `/home/user/repo/binaries/` to `/home/user/repo/staging/`.
2. Write a C++ program at `/home/user/renamer.cpp`. This program must parse `/home/user/repo/mapping.csv` and systematically rename the files inside `/home/user/repo/staging/` to their new semantic names.
3. Compile and execute your C++ program.
4. Once renamed, create a GNU `tar` incremental backup of the `/home/user/repo/staging/` directory.
   - Use the existing snapshot file `/home/user/backup/snapshot.snar`.
   - Save the backup archive as `/home/user/backup/incremental.tar.gz`.
   - Ensure the paths inside the tarball are relative to the staging directory (i.e., the tarball should contain `app-v1.0.0.bin` at its root, not `home/user/repo/staging/app-v1.0.0.bin`).

Requirements:
- Do not modify the original files in `/home/user/repo/binaries/`.
- Ensure your C++ code correctly parses the CSV and handles file operations (you may use `<filesystem>` and `<fstream>`).