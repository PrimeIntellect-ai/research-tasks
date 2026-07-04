As a technical writer, I recently inherited a documentation archive located at `/home/user/doc_backup`. Unfortunately, the automated backup tool used by the previous writer had a bug: it created infinite symlink loops within the subdirectories and accidentally compressed its own ELF executables alongside the actual documentation files.

I need you to write a C++ program at `/home/user/indexer.cpp` and compile it to `/home/user/indexer`. The program must perform the following tasks:

1. **Safe Navigation:** Recursively traverse the `/home/user/doc_backup` directory without getting trapped in symlink loops.
2. **Compressed Stream & Header Extraction:** For every `.gz` file found, inspect its uncompressed content. Read the first 4 bytes of the uncompressed data. 
3. **Filtering:** If the uncompressed file starts with the ELF magic number (`\x7fELF`), it is a compiled binary and must be ignored.
4. **Checksum & Manifest Generation:** For all non-ELF compressed files, compute the SHA256 checksum of their *uncompressed* contents. 
5. **Atomic Write:** Create a manifest file formatted as `<sha256_hash>  <relative_path_to_gz_file>` (where the relative path is relative to `/home/user/doc_backup`). Sort the entries alphabetically by the relative file path. To ensure no data corruption occurs if the program is interrupted, you must write the manifest to a temporary file first, and then atomically move it to `/home/user/manifest.txt`.

Please write, compile, and execute the C++ program so that `/home/user/manifest.txt` is generated correctly. You may use shell commands to invoke your compiler and execute the binary, and your C++ code may shell out to standard Linux utilities (like `zcat` or `sha256sum`) if that simplifies the stream processing and checksum generation.