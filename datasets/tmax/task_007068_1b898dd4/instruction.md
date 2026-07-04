You are a developer organizing a messy repository of binary assets for a project. The directory `/home/user/project_blobs` contains various files in nested subdirectories. Many files have incorrect, missing, or misleading file extensions. 

Your task is to identify specific archive files based on their binary headers, deduplicate them, organize them using hard links, and generate a checksum manifest.

Perform the following steps:
1. Search recursively through `/home/user/project_blobs/` for files that are valid ZIP archives. You must identify them strictly by their binary header (magic number: `50 4b 03 04` at the very beginning of the file). Ignore file extensions entirely, as some `.zip` files might be fake and some valid zips might be named `.dat` or have no extension.
2. Create a new directory at `/home/user/organized_zips/`.
3. Calculate the SHA-256 checksum of every valid ZIP file you found.
4. For each unique ZIP file (based on its checksum), create exactly one hard link in `/home/user/organized_zips/`. The hard link must be named `<sha256_checksum>.zip`. If there are multiple identical zip files, just link to one of them.
5. Create a manifest file at `/home/user/zip_manifest.txt` containing the SHA-256 checksums and file sizes of the unique zips you organized. The format of each line should be: `<sha256_checksum> <size_in_bytes>` sorted alphabetically by the checksum.

Constraints:
- You must write a Bash script or use Bash shell commands to accomplish this.
- Ensure only actual ZIP files (based on the magic bytes) are processed.
- Use hard links, not symbolic links or file copies.