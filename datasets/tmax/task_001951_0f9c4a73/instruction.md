You are an IT backup administrator tasked with archiving specific text logs from a legacy system. The system outputs logs in UTF-16LE encoding, but your new storage system requires them to be in UTF-8. You also need to perform an incremental backup and generate a custom manifest using a C program.

Here is your task:

1. **Write a C program** at `/home/user/hasher.c` and compile it to `/home/user/hasher`.
   - The program must accept exactly one command-line argument: the name of a file.
   - It must read data continuously from `stdin` until EOF.
   - As it reads, it must write the exact same data to `stdout`.
   - It must calculate an 8-bit XOR checksum of all the bytes read from `stdin` (initialize an `unsigned char` at 0, and XOR it with every byte read).
   - After reaching EOF, it must append a line to `/home/user/manifest.txt` in the exact format: `[HEX] [filename]\n` where `[HEX]` is the 2-digit uppercase hexadecimal representation of the XOR checksum (e.g., `3F`), and `[filename]` is the command-line argument passed to it.

2. **Perform an incremental backup** of the directory `/home/user/legacy_logs/`.
   - Find all files in `/home/user/legacy_logs/` that have been modified *more recently* than the timestamp file `/home/user/last_backup.stamp`.
   - For each of these newer files, perform the following in a pipeline:
     a) Read the file.
     b) Convert its contents from UTF-16LE to UTF-8 using `iconv`.
     c) Pipe the UTF-8 output into your `/home/user/hasher` program, passing the base filename (e.g., `log1.txt`) as the argument.
     d) Append the standard output of the hasher to a single concatenated archive file located at `/home/user/archive.bin`.
   - Process the newer files in alphabetical order.

Ensure your compiled program is named `/home/user/hasher` and that after your operations, `/home/user/manifest.txt` and `/home/user/archive.bin` contain the correct checksums, filenames, and UTF-8 concatenated data respectively.