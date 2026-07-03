As a storage administrator, I'm dealing with a custom archive format used by our legacy video processing system. We recently discovered that our current extraction tool is vulnerable to path traversal attacks (similar to "Zip Slip"), allowing maliciously crafted archives to overwrite critical system files outside the intended extraction directory.

I need you to write a secure C++ extractor at `/home/user/secure_extractor.cpp` that reads this custom archive format and safely extracts it.

The custom archive is provided via standard input (`stdin`) and consists of sequential file entries. Each entry is encoded exactly as follows (no padding):
1. A 2-byte unsigned integer (little-endian) representing the length of the filename ($L$).
2. $L$ bytes representing the filename (ASCII string).
3. A 4-byte unsigned integer (little-endian) representing the file size in bytes ($S$).
4. $S$ bytes of raw file data (binary).
This sequence repeats until EOF.

Requirements for your C++ program:
1. It must take exactly one command-line argument: the target extraction directory.
2. It must read the archive stream from standard input.
3. It must detect path traversal attempts. A filename is considered malicious if it attempts to write outside the target directory (e.g., contains `../`, `..\\`, starts with `/`, starts with `\`, or resolves to a higher-level directory).
4. If an archive contains *any* malicious filename, the program must reject the entire archive, safely remove any files it has already extracted from this archive during the run (rollback), print exactly `MALICIOUS` to standard output, and exit with status code 1.
5. If the archive is entirely clean, it must extract all files into the target directory, print exactly `CLEAN` to standard output, and exit with status code 0.
6. Compile your code to an executable at `/home/user/secure_extractor`.

Please ensure it handles binary file data correctly, as some of our clean archives contain chunks of video data.