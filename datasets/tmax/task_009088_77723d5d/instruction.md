You are an artifact manager tasked with curating a set of binary repositories. Your system has received a compressed artifact bundle and a messy manifest file, and you need to build a custom archiver in C to package the extracted files into a specific chunked binary format.

Follow these steps exactly to complete the task:

**Phase 1: Extraction and Cleanup**
1. You have a tarball located at `/home/user/repo/bundle.tar.gz` and a raw text manifest at `/home/user/raw_manifest.txt`.
2. Extract `/home/user/repo/bundle.tar.gz` into the directory `/home/user/unpacked/`. Inside the tarball, you will find some files and a nested archive (`nested.zip`). Extract the contents of `nested.zip` directly into `/home/user/unpacked/` as well.
3. Use shell utilities (like `sed` or `awk`) to process `/home/user/raw_manifest.txt`. Remove all comments (anything starting with `#`), remove all blank lines, and trim leading/trailing whitespace. Save the cleaned output to `/home/user/clean_manifest.txt`.

**Phase 2: Custom C Archiver**
Write a C program at `/home/user/archiver.c` and compile it to `/home/user/archiver`.
The program must take three command-line arguments: 
`./archiver <manifest_file> <base_directory> <output_file>`

It must do the following:
1. Open the `<output_file>` for writing in binary mode.
2. Write a 4-byte magic number: `"ARTF"` (ASCII characters 'A', 'R', 'T', 'F').
3. Read the `<manifest_file>` line by line. Each line contains a relative file path.
4. For each file path:
   a. Open the corresponding file in `<base_directory>/<file_path>` for reading in binary mode.
   b. Calculate the number of 1024-byte chunks needed to store the file (the last chunk may be smaller).
   c. Write the file path length as a 2-byte unsigned integer (`uint16_t`). Use the native system endianness.
   d. Write the file path string itself (do NOT include the null terminator).
   e. Write the total number of chunks as a 4-byte unsigned integer (`uint32_t`).
   f. For each chunk (in sequential order):
      i. Write the chunk size as a 2-byte unsigned integer (`uint16_t`). This will be 1024 for all chunks except possibly the last one.
      ii. Write the actual chunk data.

**Phase 3: Execution and Verification**
1. Run your compiled program:
   `./archiver /home/user/clean_manifest.txt /home/user/unpacked /home/user/repo_archive.bin`
2. Generate the SHA-256 checksum of `/home/user/repo_archive.bin` and output ONLY the hash (no file paths or extra text) into `/home/user/archive_hash.txt`.

Ensure all file paths and permissions are correct. You do not have root access.