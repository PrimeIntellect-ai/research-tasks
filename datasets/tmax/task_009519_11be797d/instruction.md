You are tasked with organizing and archiving project data. As a developer, you need to write a custom C utility that performs an incremental backup, bulk renames files based on a configuration file, generates a manifest with checksums, and creates a final archive.

Here are the requirements:

1. **Directories and Files setup**:
   - Source data directory: `/home/user/raw_data/` (Assume this contains various files like `.png`, `.txt`, `.c`).
   - Backup directory: `/home/user/backup/` (Create this directory).
   - Configuration file: `/home/user/rules.cfg`.
   - Previous manifest file: `/home/user/manifest.txt` (Might not exist on the first run).
   - New manifest file: `/home/user/new_manifest.txt`.

2. **Configuration File Format** (`/home/user/rules.cfg`):
   The config file contains renaming rules, one per line, in the format `extension=prefix`.
   For example:
   ```
   .png=img_
   .txt=doc_
   .c=src_
   ```

3. **C Program Requirements** (`/home/user/backup_tool.c`):
   Write a C program that compiles to `/home/user/backup_tool` (use `gcc -o /home/user/backup_tool /home/user/backup_tool.c -lcrypto` if you use OpenSSL, or you can use `popen` to shell commands).
   The program must:
   - Read `/home/user/rules.cfg` to load the prefix rules.
   - Scan all regular files in `/home/user/raw_data/`.
   - Read the existing `/home/user/manifest.txt` (if it exists) to support incremental backups. The manifest format is `original_filename|mtime|sha256sum`.
   - For each file in `/home/user/raw_data/`:
     - Determine its original filename and current modification time (`mtime`).
     - If the file exists in the old manifest with the *exact same mtime*, it is unchanged. Skip copying it, but **do** write its old record (original_filename|mtime|sha256sum) to `/home/user/new_manifest.txt`.
     - If the file is new or modified (mtime differs or not in old manifest):
       - Calculate its SHA256 checksum.
       - Find its extension. If it matches a rule in `rules.cfg`, prepend the prefix to the filename (e.g., `data.png` -> `img_data.png`). If no rule matches, keep the original name.
       - Copy the file from `/home/user/raw_data/` to `/home/user/backup/` using the new name.
       - Write a new record to `/home/user/new_manifest.txt` in the format: `original_filename|mtime|sha256sum`.

4. **Archiving**:
   After running your C program, create a compressed tarball of the `/home/user/backup/` directory located at `/home/user/backup_archive.tar.gz`.

**Important execution instructions**:
Before writing your code, you should create some dummy files in `/home/user/raw_data/` and a `/home/user/rules.cfg` to test your program. Make sure you run your program at least once, touch/modify one of the source files, and run it again to ensure the incremental logic (via `manifest.txt`) works correctly. Make sure your final state includes the compiled binary, the backup directory with the renamed files, the `new_manifest.txt`, and the `backup_archive.tar.gz`. Move `new_manifest.txt` to `manifest.txt` between runs to test the incremental feature.