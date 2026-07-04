As a technical writer for a robotics manufacturing company, I am trying to organize an old dump of technical documentation. The engineers gave me a legacy archive file named `/home/user/legacy_docs.bin`. 

This archive contains a mix of standard text documentation, 3D printer calibration scripts (GCode), and compiled firmware binaries (ELF). Unfortunately, the archive uses a proprietary, custom-compressed format called "DocPack", and the original extraction tool has been lost.

I need you to write a C program that reads a DocPack archive from **standard input** (via stream redirection), parses the binary format, decompresses the files, and organizes them.

Here is the specification for the "DocPack" binary format:
1. **Magic Header:** The file starts with 4 bytes: the ASCII string `DOCP`.
2. **File Count:** The next 4 bytes are an unsigned 32-bit integer (little-endian) indicating the number of files in the archive.
3. **File Entries:** For each file, the following sequence occurs immediately one after another:
   - **Filename:** 32 bytes (ASCII, null-terminated if shorter than 32 bytes).
   - **Type ID:** 1 byte unsigned integer. (`0` = Text Document, `1` = GCode, `2` = ELF Binary).
   - **Compressed Size:** 4 bytes unsigned 32-bit integer (little-endian) indicating the length of the compressed data payload.
   - **Data Payload:** `[Compressed Size]` bytes of custom Run-Length Encoded (RLE) data.
     - The custom RLE format consists of pairs of bytes: `[Count][Value]`. 
     - `Count` (1 byte unsigned) indicates how many times the `Value` (1 byte) should be repeated in the uncompressed output.

**Your Tasks:**
1. Write a C program at `/home/user/doc_extractor.c` that implements this parser and decompressor. It must read the archive strictly from standard input.
2. Compile your C program to `/home/user/doc_extractor`.
3. Create the directory `/home/user/extracted/` and use your tool to extract the contents of `/home/user/legacy_docs.bin` into it.
4. Create a categorized directory structure at `/home/user/docs/by_type/text/`, `/home/user/docs/by_type/gcode/`, and `/home/user/docs/by_type/elf/`.
5. For every file in `/home/user/extracted/`, create a **symbolic link** in the corresponding `by_type` subdirectory based on its Type ID (Text=text, GCode=gcode, ELF=elf). The symlink name should exactly match the filename.
6. Finally, create a log file at `/home/user/manifest.txt` that lists the absolute paths of all the **symbolic links** you created, one per line, sorted alphabetically.

Ensure your code handles binary standard input correctly and handles file I/O safely. Do not use external libraries other than standard C library functions.