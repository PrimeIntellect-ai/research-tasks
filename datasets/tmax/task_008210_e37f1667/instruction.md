You are acting as a storage administrator managing disk space backups. 

We have a custom disk usage scanning tool written in Rust, located at `/home/user/scanner`. This tool is designed to recursively calculate the total size of files in given directories. However, it currently crashes with a stack overflow or hangs indefinitely when run on certain directories because it blindly follows symlinks, and we have intentional symlink loops in our data directories.

Your task is to fix the tool and run it according to our backup configuration.

Specifically, you need to:
1. Parse the configuration file at `/home/user/backup_config.conf`. It contains lines like `SCAN_DIR=/path/to/dir`. Extract all the directory paths defined by `SCAN_DIR`. Ignore comments and empty lines.
2. Edit the Rust code in `/home/user/scanner/src/main.rs`. Modify the recursive scanning logic so that it uses `fs::symlink_metadata` instead of `fs::metadata` (or otherwise correctly ignores following symlink directories). The tool should count the size of the symlink file itself, but NOT follow it to scan its target.
3. Build the Rust project using `cargo build --release`.
4. Run the compiled executable (`/home/user/scanner/target/release/scanner`) passing ALL the extracted directory paths from step 1 as command-line arguments. 
5. Redirect the standard output of the tool to `/home/user/final_sizes.txt`.

The output format of the Rust tool (when fixed) should be one line per directory argument in the format:
`<directory_path> - Total size: <total_bytes> bytes`

Ensure your final output in `/home/user/final_sizes.txt` matches this exact format for all directories listed in the config.