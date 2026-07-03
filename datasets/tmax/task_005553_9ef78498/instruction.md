You are an AI assistant acting as a storage administrator to manage disk space on a Linux server.

You have a directory of raw, nested database backups at `/home/user/backups/raw/` that are consuming too much disk space and have inconsistent naming conventions. 

Your task is to write a Bash script at `/home/user/archive_optimizer.sh` that automates the extraction, metadata-based bulk renaming, and custom re-compression of these archives. The script must process all `.tar` files in the raw directory and output the optimized results to `/home/user/backups/processed/`, while strictly using only bash built-ins, coreutils, and standard CLI tools (`tar`, `gzip`, `unzip`, `base64`, `file`, `awk`, `sed`, `grep`, etc.).

The script must perform the following pipeline for each `.tar` file found in `/home/user/backups/raw/`:

1. **Nested Archive Extraction**: Extract the `.tar` file. Inside, you will find multiple `.zip` files. Unzip all of them into a temporary workspace.
2. **Domain-Specific Parsing & Bulk Renaming**:
   - **WAL Files**: Look for all files with the `.wal` extension. These are Write-Ahead Logs. The very first line of each `.wal` file has the format `TXN: <number>` (e.g., `TXN: 8821`). Rename the `.wal` file to `txn_<number>.wal` (e.g., `txn_8821.wal`).
   - **ELF Files**: Look for all files with the `.elf` extension. Use the standard `file` command to determine if the ELF executable is 32-bit or 64-bit. Rename the file by appending `_32` or `_64` before the extension (e.g., if `dump.elf` is 64-bit, rename it to `dump_64.elf`).
3. **Custom Compression**: Once all `.wal` and `.elf` files are renamed, package ALL the extracted and renamed files (ignoring the original `.zip` files) into a new archive. You must use a custom compression chain: package the files using `tar`, compress them with `gzip -9` (maximum compression), and then encode the binary gzipped data into base64 text using the `base64` command. 
4. **Output**: Save the final base64 text stream to `/home/user/backups/processed/<original_basename>.b64gz` (for example, if the input was `db_node_A.tar`, the output must be `db_node_A.b64gz`).
5. **Cleanup**: Delete the original `.tar` file from `/home/user/backups/raw/` to free up space, and clean up your temporary workspaces.

**Requirements**:
- The script must be marked as executable and handle multiple `.tar` files in a single run.
- You must execute your script so the final state can be verified. 
- Ensure the processed directory exists before writing to it.