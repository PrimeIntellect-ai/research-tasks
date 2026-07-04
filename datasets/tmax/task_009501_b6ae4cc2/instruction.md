You are helping a developer safely apply an incremental project update from an untrusted tarball. You must write a Go program to perform this task securely, ensuring no files overwrite outside the intended directory (Zip Slip vulnerability), writes are atomic, and unchanged files are not unnecessarily modified.

Write a Go program located at `/home/user/apply_update.go`. When executed, it must do the following:

1. **Read the Archive:** Open and iterate through the uncompressed tar archive located at `/home/user/update.tar`.
2. **Prevent Zip Slip (Path Validation):** For each file header in the tarball:
   - If the file's path (header Name) contains `..` or starts with a forward slash `/`, it is considered malicious. 
   - Do NOT extract it. Instead, append the exact malicious path (the header Name) to a file at `/home/user/project/skipped.txt` (one path per line).
3. **Incremental Update logic:** For safe files, they should be extracted to `/home/user/project/`.
   - Calculate the SHA-256 checksum of the file's contents from the tar archive.
   - If the file already exists at the target path in `/home/user/project/`, calculate its SHA-256 checksum.
   - If the target file exists and its checksum matches the tarball file's checksum, **do not** modify the file or write anything to disk for this entry.
4. **Atomic Writes:** If the safe file does not exist, or its checksum differs:
   - Extract it by first writing the contents to a uniquely named temporary file inside the `/home/user/project/.tmp/` directory. (Create this `.tmp` directory if it does not exist).
   - Once the file is fully written to the temporary location, atomically rename/move it to the final target path inside `/home/user/project/`.
5. **Manifest Generation:** After all files in the tarball have been processed, generate a manifest of the current project state.
   - Scan all regular files in `/home/user/project/` and its subdirectories.
   - Exclude the `.tmp` directory, `manifest.txt`, and `skipped.txt` from the manifest.
   - Write a manifest file to `/home/user/project/manifest.txt`.
   - Each line in the manifest must be in the format `<sha256> <relative_path>` (e.g., `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 file1.txt`).
   - The paths must be relative to `/home/user/project/`.
   - The lines must be sorted alphabetically by the relative path.

Compile and run your Go program to perform the update. Ensure all final files are correctly placed in `/home/user/project/`.