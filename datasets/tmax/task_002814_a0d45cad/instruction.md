You are an AI assistant helping a technical writer manage a large documentation update process. The writer receives "update packages" that specify new versions of documentation files. However, a recent security audit revealed that some update packages contain malformed paths designed to overwrite sensitive system files (a directory traversal / "zip slip" style vulnerability).

Your task is to build a secure documentation updater in C, apply updates, perform text transformations, and generate a final manifest.

**Step 1: Write the C Updater Program**
Write a C program at `/home/user/doc_updater.c` and compile it to `/home/user/doc_updater`.
The program must take three command-line arguments: 
`./doc_updater <update_pkg_dir> <target_dir> <backup_dir>`

The `<update_pkg_dir>` contains a `manifest.txt` file. Each line in `manifest.txt` has the format:
`destination_relative_path | source_filename`
(e.g., `api/v1/auth.md | new_auth.md` or `../../secret.txt | exploit.md`)

For each line in the manifest:
1. Construct the absolute destination path by appending `destination_relative_path` to `<target_dir>`.
2. **Security Check (Zip Slip Prevention):** You MUST verify that the final resolved absolute path is strictly contained within the absolute path of `<target_dir>`. You should use standard C functions (like `realpath`) to resolve paths and check boundaries. 
   - If the path points outside `<target_dir>`, skip the file and print `SKIPPED: <destination_relative_path>` to standard output with a newline.
3. **Incremental Backup:** If the security check passes and a file already exists at the destination path, copy the existing file to `<backup_dir>/<destination_relative_path>` BEFORE overwriting it. You must create any necessary parent directories in the backup directory structure.
4. **Copy File:** Copy the `<source_filename>` (located in `<update_pkg_dir>`) to the destination path. You must create any necessary parent directories in the target directory structure.

**Step 2: Execute the Updater**
Run your program using the following directories:
- Update Package Directory: `/home/user/update_pkg`
- Target Directory: `/home/user/docs_target`
- Backup Directory: `/home/user/docs_backup` (You must create this directory first).

**Step 3: Text Transformation**
After successfully applying the updates securely, you need to rebrand the documentation.
Using tools like `sed`, `awk`, or `vim`, recursively find all `.md` and `.txt` files in `/home/user/docs_target` and replace every occurrence of the exact string `[COMPANY_NAME]` with `AcmeCorp`.

**Step 4: Generate Final Manifest**
Write a shell script at `/home/user/gen_manifest.sh` that recursively iterates through all files in `/home/user/docs_target`.
For each file, compute its SHA256 checksum. 
Save the results to `/home/user/final_manifest.txt`.
The file must be sorted alphabetically by the file path. Each line must be in the format output by the standard `sha256sum` command:
`<sha256_hash>  <absolute_file_path>`

Ensure all scripts and code are properly executed and the final state is achieved.