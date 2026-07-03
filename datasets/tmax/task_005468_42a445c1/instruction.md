You need to help me organize some messy project directories by writing a custom archiving tool in C. I have a configuration file at `/home/user/archive.conf` that lists several directories I want to back up. However, these directories are notorious for containing complex symlink loops that crash standard backup scripts. 

Your task is to write a C program at `/home/user/archiver.c` and compile it to `/home/user/archiver`. The program must do the following:

1. **Read Configuration:** Read the text file `/home/user/archive.conf`. Each line contains an absolute path to a directory that needs archiving. Ignore empty lines.
2. **Directory Traversal & Loop Prevention:** Recursively traverse each directory listed. You **must** prevent infinite loops caused by symlinks (e.g., a symlink pointing to its own parent directory). You should also ensure no file is archived more than once, even if it is reached via multiple paths or symlinks. Only archive regular files (skip directories, raw symlinks, sockets, etc., in the output archive).
3. **Custom Compression (RLE):** Read the contents of each discovered regular file and compress it using a custom Run-Length Encoding (RLE) format. 
   - The RLE format consists of pairs of bytes: `[Count][Value]`.
   - `Count` is an unsigned 8-bit integer (1 to 255) representing how many times `Value` repeats consecutively.
   - If a character repeats more than 255 times, output a pair with a count of 255, and start a new pair for the remaining characters.
   - The end of a file's compressed stream is strictly marked by the special byte pair `[0x00][0x00]`.
4. **Archive Format:** The final archive must be written to `/home/user/output.archive` with the following binary structure:
   - **Global Header:** The exact 8-byte ASCII string `RLE_ARC\n`
   - **Per-File Entries (for each regular file archived):**
     - **Path Length:** A 16-bit unsigned integer (little-endian) representing the length of the file's relative path (relative to `/home/user/`, e.g., if the file is `/home/user/project/file.txt`, the relative path is `project/file.txt`).
     - **Path String:** The relative path string (ASCII, not null-terminated, length matches the previous field).
     - **Compressed Data:** The RLE-compressed contents of the file, followed by the `[0x00][0x00]` EOF marker.

**Constraints:**
- Do not use any external compression libraries (like zlib); implement the RLE manually in C.
- Write your C code using standard POSIX/Linux APIs (e.g., `stat`, `dirent.h`).
- Run your compiled program to generate the `/home/user/output.archive` file.
- The order of files in the output archive does not matter, as long as all unique regular files are present exactly once and correctly compressed.