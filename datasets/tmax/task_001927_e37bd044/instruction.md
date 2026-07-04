You are a storage administrator working on a legacy data migration project. We need to move a large, critical binary file to an older storage appliance that has strict file-size limitations and lacks built-in data integrity checks.

Your task is to write a C program that splits a given binary file into smaller chunks, calculates a custom checksum for each chunk, and generates a text manifest.

Write your C code in `/home/user/chunker.c`, compile it, and execute it against the input file `/home/user/archive.dat`.

Here are the precise specifications for your C program:
1. **Input File:** `/home/user/archive.dat` (a binary file).
2. **Chunk Size:** Exactly 4096 bytes per chunk. The final chunk should contain whatever remainder bytes are left.
3. **Output Location:** All chunks must be written to the directory `/home/user/chunks/`. Create this directory if it does not exist.
4. **Chunk Naming:** Name the chunk files sequentially as `chunk_0000.dat`, `chunk_0001.dat`, `chunk_0002.dat`, etc.
5. **Manifest Generation:** Generate a text file at `/home/user/chunks/manifest.txt`.
6. **Manifest Format:** For each chunk generated, write exactly one line to `manifest.txt` in the following format:
   `[chunk_filename] [size_in_bytes] [xor_checksum]`
   * `[chunk_filename]` is the name of the chunk (e.g., `chunk_0000.dat`).
   * `[size_in_bytes]` is the integer size of the chunk.
   * `[xor_checksum]` is a 2-character lowercase hexadecimal string representing the XOR sum of all bytes in that chunk. (Start with an initial checksum of 0, and perform a bitwise XOR with each byte in the chunk).

Example of a valid `manifest.txt` line:
`chunk_0000.dat 4096 7f`

Please write the code, compile it, and process `/home/user/archive.dat` to generate the `/home/user/chunks/` directory and all required files.