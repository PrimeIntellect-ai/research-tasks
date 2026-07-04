You are acting as an artifact manager curating binary repositories. We receive artifact bundles as zip files, but some of these files are maliciously crafted with "zip slip" vulnerabilities (containing paths that escape the target directory, such as `../` or absolute paths). 

We need to securely extract, transform, and incrementally back up the artifacts.

Please write a Go program at `/home/user/curator.go` and execute it to perform the following operations:

1. **Secure Extraction**: Read the archive located at `/home/user/repository.zip`. Extract its contents to the directory `/home/user/extracted/`. You must strictly prevent "zip slip" attacks: ignore any file in the archive whose resolved extraction path falls outside of `/home/user/extracted/`.
2. **Format Conversion**: During or after extraction, find all valid extracted files ending with the `.hex` extension. These files contain plain text hexadecimal strings. Decode the hex strings into their raw binary bytes, save the output as a new file with the `.bin` extension in the same directory, and then delete the original `.hex` file.
3. **Manifest Generation**: After all valid files are extracted and converted, generate a JSON manifest file at `/home/user/new_manifest.json`. The manifest must map the relative file paths (e.g., `valid1.bin`, `subdir/valid3.bin`) to their SHA-256 checksums (as lowercase hex strings).
4. **Incremental Backup**: Read the previous manifest file located at `/home/user/previous_manifest.json` (which has the same format). Compare the current files with the previous manifest. Create a gzip-compressed tar archive (`tar.gz`) at `/home/user/incremental_backup.tar.gz` containing *only* the files that are new or whose SHA-256 checksums have changed compared to `previous_manifest.json`. The paths in the tar archive must be relative to `/home/user/extracted/`.

Ensure all operations are completed and the required files are present in `/home/user/`.