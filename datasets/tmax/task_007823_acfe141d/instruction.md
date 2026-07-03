You are acting as a storage administrator. Our server is running low on disk space due to massive uncompressed log files scattered across various directories. We need a custom C++ utility to find, compress, and chunk these large log files. 

Please write a C++ program at `/home/user/archiver.cpp` and compile it to `/home/user/archiver`. 

The program must perform the following tasks:
1. **Directory Traversal & Metadata Search**: Recursively traverse the directory `/home/user/logs_archive`. Look for all files that meet BOTH of the following criteria:
   - The file extension is exactly `.log`.
   - The file size is strictly greater than 10,240 bytes (10 KB).

2. **Chunking**: For each matching file, logically split the uncompressed data into chunks of exactly 5,120 bytes (5 KB). The final chunk may be smaller than 5,120 bytes.

3. **Custom Compression**: Compress the data of each chunk using a custom Run-Length Encoding (RLE) algorithm. 
   - RLE Specification: For a sequence of identical consecutive bytes, output the byte itself, followed by an 8-bit unsigned integer representing the count. 
   - The count must not exceed 255. If there are 256 identical consecutive bytes, it should be encoded as [byte][255] followed by [byte][1]. 
   - Example: The string `AAAAA` (five 'A's) becomes `0x41 0x05`. A single `B` becomes `0x42 0x01`.

4. **Output**: Save the compressed chunks into the directory `/home/user/compressed_logs/` (create this directory if it doesn't exist). 
   - The naming convention for the chunks must be: `<original_filename_without_path>.chunk<N>.rle`
   - Where `<N>` is the 0-indexed chunk number (e.g., `app.log` becomes `app.log.chunk0.rle`, `app.log.chunk1.rle`, etc.).
   - Do NOT preserve the original subdirectory structure in `/home/user/compressed_logs/`.

5. **Cleanup**: After successfully writing all compressed chunks for a given log file, delete the original log file from `/home/user/logs_archive` to free up disk space.

Do not process any files that do not match the size and extension criteria.

When you are finished, run your compiled `/home/user/archiver` program to process the files currently in `/home/user/logs_archive`. Leave the generated `.rle` files in `/home/user/compressed_logs/`.