You are an AI assistant helping a technical writer manage their documentation backups. 

The writer keeps all their documentation in the directory `/home/user/doc_repo/`. Yesterday, they took a full backup and recorded the SHA-256 checksums of all the files at that time. These checksums are stored in `/home/user/backup/full_checksums.txt`.

Since the last backup, the writer has modified several existing documents and created some new ones. They now need to create a differential backup archive.

Your task is to:
1. Identify all files in `/home/user/doc_repo/` that have either been modified (their current checksum does not match the one in `full_checksums.txt`) or are completely new (they do not appear in `full_checksums.txt` at all).
2. Using streaming I/O and standard Linux utilities, create a gzipped tarball containing ONLY these changed and new files.
3. Save this compressed differential backup to `/home/user/backup/docs_diff.tar.gz`.

Requirements:
- Do not create any intermediate uncompressed tar files or lists on disk. Use pipes or streaming capabilities directly to standard output/input to construct and compress the archive.
- Ensure the archive stores the files with their names as they appear in the `doc_repo` directory (e.g., `doc_015.txt`, not absolute paths if possible, but absolute paths are acceptable as long as the file content is correct).
- You may write a bash script or use a one-line pipeline to accomplish this.