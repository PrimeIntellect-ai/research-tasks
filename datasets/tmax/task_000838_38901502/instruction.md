As a backup administrator, you need to recover a specific database transaction from a custom backup archive (`/home/user/backup.cba`). However, the only available extraction tool (`/home/user/extractor.c`) has a known directory traversal ("Zip Slip") vulnerability. 

Your task consists of three parts:

1. **Fix the Extractor**: Modify the provided C program `/home/user/extractor.c`. You must fix the directory traversal vulnerability by ensuring that the program extracts files using *only* the base name of the file path specified in the archive. For example, if the archive specifies a file named `../../../etc/shadow`, it must be extracted locally as just `shadow`. 
2. **Extract the Archive**: Compile your fixed extractor. Create a directory named `/home/user/recovery/` and run your compiled extractor from within that directory to extract `/home/user/backup.cba`. If your fix is correct, no files will be extracted outside of `/home/user/recovery/`.
3. **Parse the WAL File**: One of the extracted files will be a Write-Ahead Log named `database.wal`. You must parse this binary file to extract a specific transaction. 
   The `database.wal` file contains a sequence of records with the following binary layout:
   - 4 bytes: Magic signature `0x4C415752` (which is 'R', 'W', 'A', 'L' in ASCII, stored as little-endian)
   - 4 bytes: Transaction ID (unsigned 32-bit integer, little-endian)
   - 4 bytes: Payload length `N` (unsigned 32-bit integer, little-endian)
   - `N` bytes: The payload data

Find the record with Transaction ID `999`. Extract its exact payload data (without any headers or trailing newlines) and save it to `/home/user/recovery/flag.txt`.

Constraints:
- You may write additional C code or use standard bash utilities (like `dd`, `hexdump`, `awk`, etc.) to parse the WAL file.
- Do not run the vulnerable `extractor.c` before fixing it, as it contains malicious paths that will corrupt your home directory.