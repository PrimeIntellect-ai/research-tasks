You are acting as a storage administrator tasked with managing and deduplicating disk space on a Linux server. You have discovered that a previous backup script failed catastrophically because it followed symbolic links into infinite loops.

Your task is to write a robust C program that traverses a directory, avoids symlink loops, compresses regular files, deduplicates identical files using hard links, and generates a manifest.

Specifically, write a C program at `/home/user/dedup_archive.c` and compile it to `/home/user/dedup_archive`.
The program must take exactly four arguments:
`./dedup_archive <source_dir> <dest_dir> <manifest_file> <error_log>`

Program Requirements:
1. **Traversal & Symlinks**: The program must recursively traverse `<source_dir>`. 
   - If it encounters a symbolic link that points to an ancestor directory (creating an infinite loop), it must NOT follow it. Instead, it should write the absolute path of the looping symlink to `<error_log>` (one path per line).
   - Ignore non-looping symlinks (do not process or archive them, just skip).
2. **Compression via Streams**: For every regular file found, compress its contents using `gzip`. You must use standard stream redirection/piping in C (e.g., using `popen` to pipe data into `gzip -c`) and write the compressed output to the corresponding relative path inside `<dest_dir>`, appending `.gz` to the filename. (e.g., `source/dir/file.txt` becomes `dest/dir/file.txt.gz`).
3. **Checksum & Manifest**: Compute the SHA256 checksum of the *uncompressed* original file. Write a line to `<manifest_file>` in the format: `<relative_path_from_source_dir> <SHA256_hash>`. (e.g., `dir/file.txt a1b2...`). Sort the final manifest file alphabetically by the relative path.
4. **Hard Link Deduplication**: If multiple regular files in the source directory have the exact same SHA256 checksum, only the first one encountered should be compressed and written as a new file. Subsequent files with the same checksum must be created in `<dest_dir>` as **hard links** to the first compressed `.gz` file, saving disk space.

Constraints & Environment:
- The source directory for your test run will be `/home/user/data_source`.
- The destination directory should be `/home/user/archive_dest`. You must create this directory and any necessary subdirectories inside it.
- The manifest should be written to `/home/user/manifest.txt`.
- The error log should be written to `/home/user/symlink_errors.log`.
- Use standard POSIX C libraries. You may use `popen` to shell out to `sha256sum` and `gzip`.

Execute your compiled program against `/home/user/data_source` and ensure `/home/user/archive_dest`, `/home/user/manifest.txt`, and `/home/user/symlink_errors.log` are correctly populated.