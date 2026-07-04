You are acting as a backup administrator managing a critical database system. You need to identify and archive specific Write-Ahead Log (WAL) files from a mixed storage directory, but you only want to archive WAL files that match a specific binary header (magic number) indicating the latest database version.

Your task is to write and execute a Python script to automate this selective archiving process.

Here are the requirements:
1. Read the configuration file located at `/home/user/backup_config.json`. This file contains two keys: 
   - `target_magic`: A string representing the 8-byte hex-escaped magic number you need to look for (e.g., "PG_WAL\\x00\\x01").
   - `output_archive`: The absolute path where you must save your final `.tar.gz` archive.
2. Recursively traverse the directory `/home/user/wal_backups`. This directory contains various WAL files. Some are uncompressed (`.wal`), some are gzip-compressed (`.wal.gz`), and some are bzip2-compressed (`.wal.bz2`).
3. For each file, you must read the **first 8 bytes of the uncompressed data**. You will need to process compressed streams on the fly to read the headers of the `.gz` and `.bz2` files without permanently extracting them to disk.
4. Compare the 8-byte header to the `target_magic` specified in the config.
5. If the header matches, add the **original** file (as it exists on disk, whether compressed or not) to a new tar.gz archive specified by `output_archive`. 
6. When adding files to the tar archive, store them at the root of the archive (i.e., do not preserve the `/home/user/wal_backups/` directory structure inside the tarball).
7. Finally, create a log file at `/home/user/archive_log.txt`. This file must contain the base filenames of all the files you successfully added to the archive, printed one per line, sorted in alphabetical order.

Ensure your script handles the binary reading and stream decompression robustly.