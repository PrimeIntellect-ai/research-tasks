You are a storage administrator dealing with a rapidly filling storage volume due to a bug in an upstream system that writes duplicate data blocks. 

We have a proprietary system that identifies unique data blocks using a custom checksum algorithm. The original source code for the checksum utility was lost, but we recovered a stripped compiled executable located at `/app/legacy_hash`. This tool takes a single file path as an argument and prints a 32-bit hex checksum.

Your task is to implement a high-performance deduplication daemon in C that can be controlled via a network socket.

Here are the requirements for your daemon:
1. **Network Service:** Write and run a C program that listens for raw TCP connections on port `8888`. 
2. **Command Handling:** The service should accept a single line of text: `DEDUP <directory_path>\n`. 
3. **Processing:** Upon receiving the command, the service must scan the specified directory for regular files.
4. **Hashing & Memory Mapping:** For each file, calculate its proprietary checksum. Because performance is critical and shelling out to `/app/legacy_hash` for thousands of files is too slow, you must reverse-engineer the hashing algorithm used by `/app/legacy_hash` (it is a very simple linear pass over the file) and implement it directly in your C code using memory-mapped I/O (`mmap`).
5. **Deduplication:** Group files by their checksum. For any group of identical files:
   - Keep the file with the lexicographically earliest filename.
   - Replace all other files in the group with a hardlink to the kept file.
   - You must do this safely: create the hardlink as a temporary file first, then atomically replace the target duplicate using `rename()`.
6. **Write-Ahead Logging (WAL):** Before performing any atomic replace, you must append an entry to `/data/dedup.wal`. You must use `flock()` to exclusively lock the WAL file while writing to prevent concurrent corruption.
   - The WAL is a strict binary format. Each entry is exactly 134 bytes:
     - Bytes 0-1: Magic bytes `0xDA 0x7A`
     - Bytes 2-5: The 32-bit checksum (little-endian)
     - Bytes 6-69: The filename of the kept file (null-padded to 64 bytes)
     - Bytes 70-133: The filename of the file being replaced (null-padded to 64 bytes)
7. **Response:** After finishing the directory, the service should reply to the TCP client with `FREED <N>\n`, where `<N>` is the total number of bytes saved (the sum of the sizes of the files that were converted to hardlinks), and then close the connection.

Write the C code, compile it (e.g., to `/app/dedup_daemon`), and run it in the background so it listens on port `8888`. Do not stop the daemon; it needs to be running for the automated tests to interact with it.