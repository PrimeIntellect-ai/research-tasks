You are a release manager preparing a minimal firmware deployment. You need to compile the source files, compute error-checking checksums, and generate a release diff against a previous version.

Your environment contains a firmware source directory at `/home/user/firmware/` with two files:
1. `boot.S` - A minimal assembly stub.
2. `app.c` - The main application logic.

Additionally, a previous manifest is located at `/home/user/manifest_v1.txt`.

Perform the following steps:

1. **Build Raw Binaries:**
   Compile both `boot.S` and `app.c` into raw binaries (`boot.bin` and `app.bin`). 
   - First, compile them to object files without linking (`-c`), using `gcc`. Do not use any optimization flags.
   - Then, use `objcopy -O binary` to extract the raw binary data from the object files into `boot.bin` and `app.bin` inside the `/home/user/firmware/` directory.

2. **Write a Checksum Utility:**
   Write a C program at `/home/user/verify.c` that computes a Fletcher-16 checksum of a given file.
   - The program should accept a file path as its first command-line argument.
   - Read the file byte-by-byte.
   - Compute Fletcher-16 using 8-bit integers initialized to 0:
     `sum1 = (sum1 + byte) % 255;`
     `sum2 = (sum2 + sum1) % 255;`
   - The final 16-bit checksum is formed by `(sum2 << 8) | sum1`.
   - The program must print the result to standard output in the exact format: `<filename>: <CHECKSUM_HEX>\n` (where `<filename>` is just the base name of the file, e.g., `boot.bin`, and `<CHECKSUM_HEX>` is exactly 4 uppercase hexadecimal characters, zero-padded).
   - Compile this program to `/home/user/verify`.

3. **Generate Manifest and Diff:**
   - Run your `verify` utility on `app.bin` and `boot.bin` (in alphabetical order).
   - Redirect the output to create a new manifest at `/home/user/manifest_v2.txt`.
   - Compare the new manifest against the old manifest using the standard `diff -u` command.
   - Save the diff output to `/home/user/release_diff.patch`.

Ensure all requested files (`verify.c`, `verify`, `manifest_v2.txt`, and `release_diff.patch`) are exactly in `/home/user/` and formatted exactly as requested.