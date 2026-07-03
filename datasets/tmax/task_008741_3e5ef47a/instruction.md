You are tasked with writing a Rust utility to safely parse, convert, and reorganize files from a legacy custom archive format, ensuring that path traversal vulnerabilities (like Zip Slip) are neutralized.

The legacy archive is located at `/home/user/data/legacy_project.pack`.

**Format of `.pack` files:**
1. **Magic Bytes:** 4 bytes `PACK` (ASCII).
2. **File Count:** 4 bytes, unsigned 32-bit integer, little-endian.
3. **File Entries** (repeated `File Count` times):
   - **Path Length:** 2 bytes, unsigned 16-bit integer, little-endian.
   - **Path:** `Path Length` bytes of UTF-8 text. *(Note: This path may contain malicious `../` sequences).*
   - **Encoding Flag:** 1 byte (0 = UTF-8, 1 = Windows-1252, 2 = UTF-16LE).
   - **File Size:** 4 bytes, unsigned 32-bit integer, little-endian.
   - **File Content:** `File Size` bytes of raw data.

**Your objectives:**
1. Create a Rust project in `/home/user/workspace/archive_tool`.
2. Write a program that reads `/home/user/data/legacy_project.pack`. For efficiency, you may use standard streaming or memory-mapped I/O (e.g., the `memmap2` crate).
3. **Prevent Zip Slip:** When extracting files, completely ignore the original directory structure. Extract *only* the base file name (e.g., `foo/../../bar/secret-File.txt` becomes `secret-File.txt`).
4. **Bulk Renaming:** Convert all extracted base file names to fully lowercase, and replace all hyphens (`-`) with underscores (`_`). For example, `secret-File.txt` becomes `secret_file.txt`.
5. **Encoding Conversion:** Read the file content based on its `Encoding Flag` and convert it to valid UTF-8. 
6. **Logging:** Keep an exact log of the sanitization process at `/home/user/workspace/extraction.log`. For every file processed (in the order they appear in the archive), append a line in exactly this format:
   `Original: <original_path> -> Sanitized: <new_base_filename>`
7. **Archive Creation:** Write the sanitized, UTF-8 encoded files directly into a new compressed tarball located at `/home/user/workspace/safe_project.tar.gz`. The tarball should contain only the files themselves at the root of the archive (no directories).

You may use third-party crates like `encoding_rs`, `tar`, `flate2`, and `memmap2`. Install them via `cargo add`. Build and run your program so that the final `safe_project.tar.gz` and `extraction.log` are successfully generated.