You are an AI assistant helping a bioinformatics researcher organize and verify a legacy dataset. 

The researcher has datasets of DNA sequences compressed using a custom Run-Length Encoding (RLE) format. The files have an `.rle` extension. Over time, some of these files may have become corrupted. You need to write a C program to verify the integrity of these files and a short shell sequence to process a list of directories.

**Custom `.rle` File Format:**
1. The file consists of a sequence of 2-byte blocks. For each block:
   - The first byte is the `count` (unsigned 8-bit integer, 1 to 255).
   - The second byte is the `character` (ASCII character, e.g., 'A', 'C', 'G', 'T').
2. The last 4 bytes of the file contain a 32-bit unsigned little-endian integer. This integer represents the **expected total length** of the uncompressed string.
3. Example: A file representing "AAACCCCT" would be `03 41 04 43 01 54 [08 00 00 00]`.

**Your Task:**
1. Write a C program at `/home/user/verify.c` and compile it to `/home/user/verify`. 
   - It should take exactly one command-line argument: the path to an `.rle` file.
   - It should read the file, compute the total uncompressed length by summing the `count` bytes, and read the expected length from the last 4 bytes.
   - If the computed length matches the expected length, print exactly `OK` to standard output.
   - If it does not match, or if the file is too short to contain a valid 4-byte trailer, print exactly `CORRUPT` to standard output.
2. The researcher has provided a configuration file at `/home/user/directories.conf`. Each line contains an absolute path to a directory.
3. Using shell commands, read `/home/user/directories.conf`. For each directory listed, recursively find all `.rle` files.
4. Run your `verify` program on each found `.rle` file.
5. Generate a final report at `/home/user/summary.log`. Each line must be in the format: `[absolute_path_to_file] [STATUS]`.
   - Example: `/home/user/data/set1/sample.rle OK`
6. Sort the final `summary.log` alphabetically by file path and save it in-place.