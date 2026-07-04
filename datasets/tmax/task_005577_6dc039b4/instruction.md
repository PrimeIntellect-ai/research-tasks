You are an artifact manager responsible for curating binary repositories. We have a backup script located at `/home/user/backup.py` that is supposed to perform an incremental backup of binary artifacts from `/home/user/artifacts` to `/home/user/backup_dest`. 

However, the current script has a few critical issues:
1. It follows symlinks blindly, which causes it to get stuck in infinite loops because our artifact repository contains circular symlink references.
2. It currently backs up files based on modification time. We need it to be smarter. Our custom `.bin` artifact files have a specific binary header. The first 4 bytes are the ASCII string `ARTF` (the magic number). The next 4 bytes are a 32-bit unsigned integer (little-endian) representing the file's version number.

Your task is to fix and complete the `/home/user/backup.py` script so that it does the following:
1. Traverses the `/home/user/artifacts` directory recursively. It MUST follow symlinks to directories, but it MUST prevent infinite loops by keeping track of the real, resolved paths of directories it has already visited. Do not process the same physical directory more than once.
2. Identifies all files ending in `.bin`.
3. Reads the binary header to extract the version number. If a `.bin` file does not start with `ARTF`, ignore it.
4. Checks if the file already exists in `/home/user/backup_dest` at the corresponding relative path (preserving the traversed directory structure, including followed symlink directory names).
5. Reads the version of the corresponding file in `/home/user/backup_dest` (if it exists and is a valid `ARTF` file).
6. Copies the file from the artifacts directory to the backup destination ONLY if the file does not exist in the destination, or if the source file's version is strictly greater than the destination file's version. Create any missing parent directories in the destination as needed.
7. Every time a file is successfully copied to the backup destination, append its absolute source path (as traversed, e.g., `/home/user/artifacts/dirA/symlink_dir/file.bin`) to `/home/user/backup.log`, one path per line.

Once you have fixed the script, execute it to perform the backup.

Constraints:
- You must write the solution in Python 3.
- Standard libraries only.
- Ensure the log file is created at `/home/user/backup.log`.