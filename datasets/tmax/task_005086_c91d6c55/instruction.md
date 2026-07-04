You are acting as an automated artifact manager. We have received a corrupted repository dump in the form of a tar archive located at `/home/user/repo_dump.tar`.

Our previous backup script crashed while processing this dump because the archive contains maliciously or accidentally crafted symlink loops. Furthermore, the repository manager lost all file extensions, leaving a bunch of binary blobs with generic names.

Your task is to curate this repository by performing the following steps:
1. Extract `/home/user/repo_dump.tar` into a new directory called `/home/user/extracted_repo/`. Be careful to handle or remove any infinite symlink loops so they don't break your scripts.
2. Analyze every standard file in `/home/user/extracted_repo/`. You must read the binary headers (magic bytes) to determine the true file type. The files will be one of three types:
   - Linux ELF Executable: Starts with `7F 45 4C 46` (`\x7FELF`)
   - PNG Image: Starts with `89 50 4E 47 0D 0A 1A 0A`
   - PDF Document: Starts with `25 50 44 46 2D` (`%PDF-`)
3. Bulk rename all standard files by appending the appropriate extension based on their actual binary content (`.elf`, `.png`, or `.pdf`). Leave the base name exactly as it was. Delete any symlinks you find in the directory.
4. Create a new, clean compressed archive containing ONLY the files identified and renamed as `.elf` executables. Save this archive to `/home/user/curated_binaries.tar.gz`. Do not include the directory structure (the `.elf` files should be at the root of the archive).
5. Generate a report of the curated ELF binaries. Create a text file at `/home/user/artifact_report.txt` containing the SHA256 hashes of all the `.elf` files you added to the new archive. The format of the file must be exactly:
`<sha256_hash>  <filename.elf>`
Sort the lines of this text file alphabetically by the SHA256 hash.

Ensure the final state matches these requirements precisely.