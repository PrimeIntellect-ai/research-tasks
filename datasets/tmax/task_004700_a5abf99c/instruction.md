You are acting as a backup administrator. We need to archive a critical application data directory, but we have strict compliance and storage requirements. 

The source data is located at `/home/user/data_to_backup`. It contains a mix of text-based log files and binary data spread across multiple subdirectories.

Your task is to write and execute a script (you can use Python, Bash, or a combination) that performs the following steps:

1. **Manifest Generation**: Recursively traverse `/home/user/data_to_backup` and calculate the SHA256 checksum for every file. Save these checksums in a manifest file at `/home/user/manifest.txt`. The format must exactly match the output of the standard `sha256sum` command (i.e., `[hash]  [relative_path_from_data_to_backup]`). Example line: `d2d2d2...  logs/app.log`.

2. **Selective Compression**: 
   - Create a staging directory at `/home/user/staging_backup`.
   - Replicate the exact directory structure of `/home/user/data_to_backup` inside `/home/user/staging_backup`.
   - For all text files (defined strictly as files ending in `.log` or `.txt`), compress them using `gzip`. Write the compressed output to the corresponding location in the staging directory, appending `.gz` to the filename (e.g., `logs/app.log` becomes `logs/app.log.gz` in the staging directory).
   - For all binary files (defined strictly as files ending in `.bin` or `.dat`), copy them exactly as they are to the staging directory without compression.

3. **Final Archival**:
   - Create a final tar archive of the staging directory.
   - The archive must be located at `/home/user/final_backup.tar` (uncompressed tar).
   - The archive should contain the contents of the staging directory such that extracting it directly yields the subdirectories (e.g., `logs/`, `binaries/`), not a top-level `staging_backup` folder.
   - Finally, append the `/home/user/manifest.txt` file into the root of this existing `/home/user/final_backup.tar` archive.

Do not use root/sudo. Make sure all paths and output formats are exactly as specified.