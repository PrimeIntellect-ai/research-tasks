As an artifact manager, I need you to curate a binary repository located at `/home/user/repo`. 
There are several files in this directory. Some are valid custom artifacts, others are corrupted, old, or not artifacts at all.

A valid custom artifact has the following binary structure:
- Offset 0: Magic number, 4 bytes, ASCII "ARTF" (`0x41 0x52 0x54 0x46`).
- Offset 4: Timestamp, 4 bytes, unsigned 32-bit integer, little-endian.
- Offset 8: Payload size (N), 4 bytes, unsigned 32-bit integer, little-endian.
- Offset 12: Payload, N bytes.
- Offset 12+N: Checksum, 1 byte. The checksum is calculated as the arithmetic sum of all payload bytes modulo 256.

I need you to write a C program that:
1. Iterates over all files in the `/home/user/repo` directory.
2. Parses each file to determine if it is a valid artifact. A file is valid if and only if:
   - It has the correct magic number.
   - The checksum exactly matches the payload.
   - The total file size is exactly `13 + N` bytes.
3. For valid artifacts ONLY, checks if the metadata timestamp is greater than or equal to `1700000000`.
4. If a valid artifact meets the timestamp criteria, it must be format-converted: extract the binary payload and write it as a continuous uppercase hexadecimal string (no spaces or newlines) to a new file in `/home/user/export/`. You should create the `/home/user/export/` directory if it doesn't exist. The output file must have the same base name as the original file, but with a `.hex` extension (e.g., `data.bin` becomes `/home/user/export/data.hex`).
5. Generates a manifest file at `/home/user/manifest.csv` containing only the curated files that were exported. Each line must be formatted exactly as: `filename,timestamp,payload_size`. The filename should just be the base name of the original file (e.g., `data.bin`). The manifest rows must be sorted alphabetically by filename.

Please compile your C program, run it, and ensure that both the `/home/user/export/` directory and the `/home/user/manifest.csv` file are successfully created according to the specifications.