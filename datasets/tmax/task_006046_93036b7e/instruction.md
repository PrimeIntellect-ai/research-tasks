You are an artifact manager maintaining a binary software repository. You recently received a binary artifact index file from an untrusted upstream source. Security analysis indicates that this index may contain path traversal attacks (similar to "zip slip" vulnerabilities), where filenames contain `../` sequences to overwrite files outside the intended extraction directory.

Your task is to write a C program at `/home/user/sanitize.c` that parses this binary index, sanitizes any malicious paths, and safely writes out a cleaned version of the index.

### Input File Format
The input file is located at `/home/user/artifacts/index.bin`.
It is a custom binary format defined as follows:
1. **Header**: Exactly 12 bytes containing the ASCII string `ARTIFACT_v1\0` (null-terminated).
2. **Records**: A sequence of records until the end of the file. Each record consists of:
   - `name_len` (16-bit unsigned integer, little-endian): The length of the filename.
   - `name` (Array of ASCII characters): The filename itself. It is exactly `name_len` bytes long and is **not** null-terminated.
   - `offset` (32-bit unsigned integer, little-endian): The byte offset of the file data in the archive.
   - `size` (32-bit unsigned integer, little-endian): The size of the file data.

### Processing Requirements
Write and execute a C program that performs the following:
1. Opens and reads `/home/user/artifacts/index.bin`.
2. Verifies the header. If invalid, the program should exit.
3. Iterates through all records.
4. Checks each `name` for the exact substring `../`. 
5. For any `name` containing `../`, sanitize it by replacing *every* instance of `../` with `___` (three underscores). (Note: This keeps the `name_len` exactly the same, simplifying the binary rewrite).
6. Safely writes the header and all records (with sanitized names, if modified, and untouched otherwise) to a temporary file `/home/user/artifacts/index_clean.bin.tmp`.
7. Once the entire file is written successfully, use an atomic operation (e.g., `rename()`) to rename the temporary file to `/home/user/artifacts/index_clean.bin`.
8. Logs the changes. For every filename that was modified, append a line to `/home/user/artifacts/sanitized.log` in exactly this format:
   `[ORIGINAL] -> [SANITIZED]`
   (e.g., `bin/../evil.sh -> bin/___evil.sh`)

Compile your C program, run it, and ensure that both `index_clean.bin` and `sanitized.log` are correctly generated.