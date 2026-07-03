You are a storage administrator tasked with managing disk space on a heavily utilized server. You need to archive older log files, split the archive to fit into constrained backup storage, and create a utility script to verify the backup can be successfully restored.

Perform the following operations:

1. Look in the directory `/home/user/logs/`. You will find several log files named with the pattern `app_YYYYMMDD.log`.
2. Identify all log files from the year 2022 (e.g., `app_2022*.log`).
3. Create a compressed tarball (`.tar.gz`) containing ONLY these 2022 log files. When archiving, ensure the files are stored at the root of the archive (do not include the `logs` directory structure).
4. Since the backup storage system has strict file size limits, split this tarball into chunks of exactly 2 Megabytes (2097152 bytes). Place the resulting chunks in `/home/user/archived_chunks/` and name them with the prefix `archive.part.` (so they will be named `archive.part.aa`, `archive.part.ab`, etc.).
5. To ensure data integrity, write a Bash script at `/home/user/restore.sh` that performs the reverse operation. The script must:
   - Reconstruct the full tarball from the chunks in `/home/user/archived_chunks/`.
   - Extract the contents into the directory `/home/user/restored_logs/`.
   - Compute the SHA256 checksums of all extracted `.log` files in `/home/user/restored_logs/`.
   - Save these checksums to `/home/user/restored_checksums.txt` in the standard `sha256sum` output format (`<hash>  <filename>`), but strictly containing only the filename (no path) and sorted alphabetically by the filename.
6. Make `/home/user/restore.sh` executable and run it to perform the restoration and generate the `/home/user/restored_checksums.txt` file.