I need you to help organize my project files by creating an incremental-style backup system with a custom compression step.

I have an active data directory at `/home/user/data` and an older backup at `/home/user/backup_v1`.

Please perform the following steps:

1. **Text Transformation**: Use `sed` to modify the file `/home/user/data/file3.txt`. Replace all occurrences of the string "v1" with "v2" in place.
2. **Incremental Backup & Custom Compression via Rust**: Write a Rust program at `/home/user/archive.rs` and compile it to `/home/user/archive`. When executed, this program should create a new directory `/home/user/backup_v2` and process every file from `/home/user/data` into it:
   - Check if a file with the exact same name and content exists in `/home/user/backup_v1`.
   - If it does, create a **hard link** to the `/home/user/backup_v1` file in `/home/user/backup_v2`.
   - If it does NOT exist in the old backup (or the content differs), write a "compressed" version of the file to `/home/user/backup_v2`. Our custom compression format simply reverses the characters of each line. The destination file should have `.rev` appended to its name (e.g., `file3.txt.rev`).
3. **Link Management**: Create a symbolic link at `/home/user/backup_latest` that points exactly to `/home/user/backup_v2`.

Run your compiled Rust program to perform the backup, then create the symbolic link. Ensure all paths and filenames are exactly as specified.