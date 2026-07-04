You are an AI assistant acting as a technical writer's automation tool. A technical writer has a set of messy documentation drafts and large binary asset files that need to be normalized, chunked, and packaged for a legacy distributed Content Management System (CMS).

Your task is to write a C++ program and execute the necessary shell commands to organize these files according to the CMS's strict requirements.

The raw files are located in `/home/user/drafts`.
Inside this directory, there are multiple `.txt` documentation files and `.dat` binary asset files.

Phase 1: Write a C++ program `/home/user/process_docs.cpp` (and compile it to `/home/user/process_docs`) that performs the following file operations on the `/home/user/drafts` directory:
1. **Bulk Renaming:** Find all `.txt` files. Sort them alphabetically by their current filename, and rename them sequentially to `doc_01.txt`, `doc_02.txt`, `doc_03.txt`, etc.
2. **File Chunking:** Find all `.dat` files. The CMS cannot handle large binaries. Split each `.dat` file into chunks of exactly 100,000 bytes (the final chunk may be smaller). The output chunks must be named `<original_filename>.chunk001`, `<original_filename>.chunk002`, etc. (1-indexed, padded to 3 digits). Delete the original `.dat` files after successful chunking.
3. **Manifest Generation:** Generate a manifest file at `/home/user/drafts/manifest.tsv`. For every file currently existing in the directory (the newly renamed `.txt` files and the `.dat.chunkXXX` files), write a line containing the filename, its size in bytes, and its SHA-256 checksum, separated by tabs. 
   - Format: `filename<TAB>size<TAB>sha256`
   - The manifest should be sorted alphabetically by filename.
   - You may use standard C++ features and `popen` or `std::system` to call command-line tools like `sha256sum` if needed.

Phase 2: Archiving
Once your C++ program has successfully transformed the directory and created the manifest, use Bash commands to package the entire contents of `/home/user/drafts` (including the manifest, but NOT the directory structure itself, just the files) into a compressed archive located at `/home/user/release.tar.gz`.

Constraints:
- All file operations, renaming, chunking, and manifest generation MUST be done by the compiled C++ program `/home/user/process_docs`.
- Do not leave any temporary files in `/home/user/drafts`.