As a storage administrator, you need to archive old application logs to free up disk space. However, a broken backup script previously created several circular symlinks within the data directory (`/home/user/app_data`), which causes standard recursive archiving tools (like `tar` or `find`) to hang or fail by following infinite loops.

Your task is to write and execute a Python script at `/home/user/archive_logs.py` that safely bypasses this issue. 

The script must:
1. Recursively traverse `/home/user/app_data`.
2. Find all regular files ending with the `.log` extension.
3. Explicitly **ignore** all symbolic links (both file and directory symlinks) to avoid infinite loops.
4. Calculate the SHA256 checksum for every valid `.log` file it finds.
5. Create a text manifest at `/home/user/manifest.txt` containing the checksums and absolute paths of the files. Each line must be formatted exactly as: `<SHA256_HASH> <ABSOLUTE_PATH>`, with a single space between them. The lines in the manifest must be sorted alphabetically by the absolute path.
6. Create an uncompressed tar archive at `/home/user/clean_logs.tar` containing all the discovered valid `.log` files. The files should be stored in the archive using their absolute paths.

Run your script so that `/home/user/manifest.txt` and `/home/user/clean_logs.tar` are generated.