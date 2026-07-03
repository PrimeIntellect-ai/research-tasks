You are a backup administrator responsible for managing a custom incremental backup system. We have received a backup archive in a proprietary format, and we need to extract it and reconstruct the final data. However, we suspect that some archives might be malicious and attempt to overwrite system files outside the extraction directory (a "zip slip" attack).

Your task is to write a C++ program that securely extracts this custom archive and reconstructs the latest backup state.

**Archive Format (`/home/user/backup.bin`)**
The archive is a flat binary file containing a sequence of file records. Each record consists of:
1. A 16-bit unsigned integer (little-endian) representing the length of the filename (`N`).
2. A string of `N` characters representing the filename.
3. A 32-bit unsigned integer (little-endian) representing the size of the file data (`S`).
4. `S` bytes of raw file data.

**Requirements:**
1. **Write a C++ program** at `/home/user/extractor.cpp`.
2. The program should accept two arguments: the path to the archive, and the output directory.
   Example: `./extractor /home/user/backup.bin /home/user/out/`
3. **Memory-Mapped I/O:** You must use POSIX memory-mapped I/O (`mmap`) to read the input archive.
4. **Security (Zip Slip Prevention):** As you iterate through the archive, extract the files to the output directory. If a filename contains the substring `..` or starts with `/`, **skip** that record entirely and do not extract it to prevent path traversal attacks.
5. **Incremental Reconstruction:** The archive contains two valid files: `base.dat` (the full backup) and `patch.dat` (the differential backup). After securely extracting the valid files, your program must read `base.dat` and `patch.dat`, apply the differential patch by performing a byte-by-byte XOR operation between them (`restored[i] = base[i] ^ patch[i]`), and save the final reconstructed data to `restored.dat` in the output directory. Both `base.dat` and `patch.dat` will be the exact same size.
6. Compile your code to `/home/user/extractor` and run it to process `/home/user/backup.bin`, extracting into the `/home/user/out/` directory.

Create the `/home/user/out/` directory before running your program.