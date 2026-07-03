You are a storage administrator managing a server's disk space. You have received a series of compressed incremental backups from a legacy system. However, automated security scanners have flagged that some of these archives might have been tampered with to exploit a "Zip Slip" vulnerability (containing absolute paths or relative paths with `../` intended to overwrite files outside the restoration directory).

Your task is to write a robust Bash script at `/home/user/process.sh` to safely process these incremental backups.

The script must take two arguments: the input directory containing the backups, and the output directory for restoration.
Example: `bash /home/user/process.sh /home/user/backups /home/user/restored`

Requirements for your script:
1. Find all `.tar.gz` files in the input directory and process them in alphabetical order.
2. For each archive, stream its table of contents (without extracting it to disk first) to identify any malicious paths. A malicious path is defined as any file path that starts with `/` (absolute) or contains `../` anywhere in the path.
3. Append any identified malicious paths exactly as they appear in the archive to `/home/user/malicious_paths.log` (one path per line).
4. Safely extract ONLY the non-malicious (valid) files from the compressed stream into the output directory (`/home/user/restored`). Files from later incremental backups should overwrite older files if they have the same name.
5. After successfully extracting the valid files from each archive, calculate the total disk space (in bytes) used by the output directory. Append a line to `/home/user/growth.log` in this exact format: `<archive_filename>: <size_in_bytes>` (e.g., `inc_01.tar.gz: 4096`). Use `du -sb <dir> | cut -f1` for consistency.

Once your script is written, run it against the `/home/user/backups` directory, extracting to `/home/user/restored`. Ensure `/home/user/malicious_paths.log` and `/home/user/growth.log` are correctly generated.