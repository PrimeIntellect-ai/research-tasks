I am a storage administrator trying to reclaim disk space by identifying orphaned blob files. Our custom database writes custom Write-Ahead Log (WAL) files, and I need a fast tool to extract the Object IDs of all "DROP" operations.

Please write a C++ program at `/home/user/extract_drops.cpp` that finds and parses all `.wal` files in the `/home/user/wal_archive/` directory.

The custom WAL format is binary and structured as follows:
1. **File Header**: 8 bytes, always containing the ASCII string `WALv1` followed by three null bytes (`\0\0\0`).
2. **Records**: A sequence of records following the header until the end of the file. Each record consists of:
   - **Timestamp**: 8 bytes (unsigned 64-bit integer, little-endian).
   - **Operation Type**: 1 byte (unsigned 8-bit integer). 
     - `0x01` = INSERT
     - `0x02` = UPDATE
     - `0x03` = DROP
   - **Object ID**: 4 bytes (unsigned 32-bit integer, little-endian).
   - **Payload Length**: 4 bytes (unsigned 32-bit integer, little-endian).
   - **Payload**: Variable length bytes (exactly the number of bytes specified by Payload Length).

**Requirements for your C++ program:**
1. You must use `mmap` (memory-mapped I/O) to read the file contents efficiently, as these logs can theoretically be very large and are actively rotated.
2. It must process all files with the `.wal` extension in `/home/user/wal_archive/`.
3. It must extract the Object ID of every `DROP` (Type `0x03`) operation found across all files.
4. It must output the unique Object IDs to `/home/user/dropped_objects.txt`. The IDs should be written one per line, printed as standard decimal integers, and sorted in ascending numerical order.

Write, compile, and execute the C++ program to produce `/home/user/dropped_objects.txt`. Use `g++ -O3 /home/user/extract_drops.cpp -o /home/user/extract_drops` to compile.