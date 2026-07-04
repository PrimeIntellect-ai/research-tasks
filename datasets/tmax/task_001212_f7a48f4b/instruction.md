You are a backup administrator tasked with recovering specific files from a corrupted legacy archive format. 

You have been provided with a raw binary archive file at `/home/user/raw_data.bin` and a configuration file at `/home/user/backup.conf`.

The custom archive format consists of a series of concatenated file entries. Each entry has the following structure:
1. Magic Number: `BKUP` (4 bytes, ASCII)
2. Filename Length: 2 bytes (unsigned 16-bit integer, little-endian)
3. Filename: variable length ASCII string (length specified above)
4. File Size: 4 bytes (unsigned 32-bit integer, little-endian)
5. File Data: raw bytes (length specified above)

The configuration file `/home/user/backup.conf` contains a list of file extensions that need to be recovered, one per line (e.g., `.log`).

Your task is to:
1. Write a C program at `/home/user/extractor.c` that parses the configuration file to determine which file extensions to extract.
2. The C program MUST use `mmap` (memory-mapped I/O) to read and parse `/home/user/raw_data.bin`. Do not use standard `read()` or `fread()` for the binary archive.
3. For every file in the archive whose filename ends with an extension listed in `backup.conf`, the program must extract its "File Data" payload and write it directly to `stdout` (standard stream redirection). Do not write headers or filenames to stdout, only the concatenated raw binary payloads of the matched files in the order they appear in the archive.
4. Compile your program to `/home/user/extractor` (e.g., `gcc -O2 /home/user/extractor.c -o /home/user/extractor`).
5. Run your program and redirect its stdout to `/home/user/extracted_logs.bin`. 

For example, your execution command should look like:
`/home/user/extractor /home/user/raw_data.bin /home/user/backup.conf > /home/user/extracted_logs.bin`

Ensure your C program cleanly handles edge cases and strictly checks the `BKUP` magic number before reading an entry. If a magic number is missing where one is expected, the program should stop processing and exit gracefully.