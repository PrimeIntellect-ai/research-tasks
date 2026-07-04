You are an AI assistant helping a technical writer organize documentation for a hardware project. The writer has an archive file containing 3D printing instructions (GCode) embedded within a custom compressed format. 

Another process periodically updates this archive, so it must be accessed safely.

Your task is to write a C program that:
1. Opens `/home/user/docs_archive.bin` for reading.
2. Acquires a shared lock (read lock) on the file using `flock(fd, LOCK_SH)` to prevent concurrent writes while reading.
3. Reads and decompresses the custom Run-Length Encoded (RLE) data. The RLE format consists of consecutive 2-byte pairs: `[1 byte unsigned count][1 byte ASCII character]`. For example, `0x03 0x41` means "AAA".
4. Parses the decompressed text as GCode to find all `G1` commands (linear moves) that include an extrusion value (`E`). 
5. Calculates the sum of all `E` values found on `G1` lines. (Assume relative extrusion, so you just sum the values directly. Example: `G1 X10 Y10 E1.5` adds 1.5 to the total).
6. Releases the lock and closes the file.
7. Writes the total extrusion value as a floating-point number formatted to exactly two decimal places to `/home/user/extrusion_report.txt`.

Constraints:
- You must write the solution in C and save it to `/home/user/analyzer.c`.
- Compile it to `/home/user/analyzer` and execute it.
- Your C code *must* include file locking via `<sys/file.h>` and `flock`.
- The output file `/home/user/extrusion_report.txt` must contain only the final sum, e.g., `12.34`.