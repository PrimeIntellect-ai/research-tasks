You are acting as a backup administrator managing an archival system. We have highly compressible, actively written log files that need to be safely backed up into a custom binary archive format.

Your task is to write a C program that reads a configuration file, securely maps and compresses the specified log files using a custom Run-Length Encoding (RLE), and writes them to a single archive file.

Here are the specific requirements:

1. **Configuration**: 
   Read the file `/home/user/backup.conf`. It contains absolute paths to the log files that need to be archived, one path per line.

2. **File Locking and Memory-Mapped I/O**:
   For each file listed in the configuration:
   - Open the file.
   - Acquire a shared lock using `flock(fd, LOCK_SH)` to ensure you don't read while a writer is modifying it.
   - Map the entire file into memory read-only using `mmap()`.
   - After processing, `munmap()`, release the lock using `flock(fd, LOCK_UN)`, and close the file.

3. **Custom RLE Compression**:
   Process the mapped data in memory and compress it using this exact Run-Length Encoding specification:
   - The output must be a sequence of 2-byte pairs: `[Count][Byte]`.
   - `Count` is an 8-bit unsigned integer (`uint8_t`) representing the number of consecutive identical bytes (from 1 to 255).
   - `Byte` is the actual byte value.
   - If a sequence of identical bytes exceeds 255, it must be split into multiple pairs (e.g., 258 'A's becomes `[255]['A'] [3]['A']`).

4. **Archiving**:
   Write the compressed 2-byte pairs for all files sequentially into `/home/user/archive.bin`. Do not include any file headers or separators between files in the archive; just append the compressed data sequentially. Open this output file for writing/creating/truncating at the start of your program.

Write your C source code to `/home/user/archiver.c`, compile it to `/home/user/archiver` using `gcc`, and then execute it. 

Do not modify the original log files or the configuration file. Ensure your C program executes without errors and successfully creates `/home/user/archive.bin`.