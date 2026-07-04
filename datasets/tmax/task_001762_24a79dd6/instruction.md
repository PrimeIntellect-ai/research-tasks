You need to develop a Rust utility that acts as an incremental configuration backup manager. We have a configuration directory at `/home/user/configs` that contains various `.conf` files, subdirectories, and symlinks. Unfortunately, there is a symlink loop in this directory that causes naive backup scripts to hang or crash.

Your task is to create a Rust program in `/home/user/tracker` (initialize it with `cargo new tracker` inside `/home/user`) that performs a safe, incremental, and redacting backup.

Requirements for the Rust program:
1. **Command Line Arguments:** The program must accept exactly three arguments: `tracker <src_dir> <dest_dir> <timestamp_seconds>`
2. **Navigation & Loop Prevention:** It must recursively traverse `<src_dir>` to find all `.conf` files. It must follow symlinks, but it **must** detect and prevent symlink loops (e.g., by tracking visited directory paths or inodes) so it doesn't get stuck in an infinite loop.
3. **Change Detection (Incremental Backup):** It should only process `.conf` files whose Unix modification timestamp is strictly greater than the `<timestamp_seconds>` provided as the third argument.
4. **Text Transformation (Redaction):** For each modified `.conf` file, read its contents. If there are any lines that start exactly with `PASSWORD=` (e.g., `PASSWORD=secret123`), replace the entire value with `REDACTED` so the line becomes exactly `PASSWORD=REDACTED`. All other lines must remain unchanged.
5. **Backup:** Write the processed file to the `<dest_dir>`, preserving the relative directory structure from `<src_dir>`. For example, if `<src_dir>` is `/home/user/configs` and you process `/home/user/configs/subdir/app.conf`, it should be saved to `<dest_dir>/subdir/app.conf`. Create any necessary intermediate directories in `<dest_dir>`.

After you write and compile the Rust program (using `cargo build`), run it with the following parameters:
- Source directory: `/home/user/configs`
- Destination directory: `/home/user/backup`
- Timestamp: `1700000000`

Ensure the final compiled binary is located at `/home/user/tracker/target/debug/tracker` and that you execute it successfully so the `/home/user/backup` directory is populated correctly.