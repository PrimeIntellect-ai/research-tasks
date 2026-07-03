You are helping a technical writer organize and verify documentation contributed by external sources. You have received a compressed tarball of documentation files, but you suspect it might contain malicious paths intended to overwrite files outside the target directory (a "Zip Slip" vulnerability), or include non-documentation files.

Your task is to write a Rust command-line tool that safely extracts this archive, filters the contents, uses atomic writes, and generates a checksum manifest.

**Requirements:**
1. Create a Rust project in `/home/user/doc_extractor`. You may use standard crates like `tar`, `flate2`, and `sha2`. 
2. The tool must read `/home/user/docs_incoming/docs.tar.gz` and extract its contents into `/home/user/docs_safe/`.
3. **Zip Slip Prevention:** Iterate over the archive entries. If an entry's path is absolute (starts with `/`) or contains `..` anywhere in its components, you must **not** extract it. Instead, print exactly `WARNING: Zip Slip detected in <path>` to `stderr`.
4. **File Filtering:** Only extract files with `.md` or `.txt` extensions. Ignore all other files.
5. **Atomic Writes:** For every valid file to be extracted, you must first write the contents to a temporary file named `<filename>.tmp` in its destination directory, and then rename it to the final `<filename>` to ensure the file is written atomically. Create any necessary parent directories inside `/home/user/docs_safe/`.
6. **Manifest Generation:** After extracting all valid files, generate a SHA-256 checksum manifest of all the extracted files. Save this manifest to `/home/user/docs_safe/manifest.txt`. The manifest must be formatted exactly as the output of the `sha256sum` command (e.g., `<hash>  <relative_path>`), and the lines must be sorted alphabetically by the relative path.

**To complete the task:**
- Write and compile the Rust tool.
- Run it to process `/home/user/docs_incoming/docs.tar.gz` into `/home/user/docs_safe/`.
- Ensure `/home/user/docs_safe/manifest.txt` is created correctly.

Do not assume you have root access. You can use standard terminal commands and write code as needed.