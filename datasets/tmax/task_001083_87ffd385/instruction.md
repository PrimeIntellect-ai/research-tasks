We are migrating our artifact management system and need a highly performant, robust archive packer written in C. Our repositories are massive and often contain corrupted structures, including infinite symlink loops left by previous backup scripts. 

Your task is to write a C program, saved at `/home/user/safe_packer.c` and compiled to `/home/user/safe_packer`, that reliably traverses a target directory and packs its files into a custom chunked archive format. 

Requirements:
1. **Directory Traversal & Cycle Detection:** Traverse the directory provided as the first command-line argument. You must detect and skip infinite symlink loops. Do not follow a symlink if it resolves to an ancestor directory currently being traversed.
2. **Chunking:** Files larger than 50 KB (51,200 bytes) must be split into multiple 50 KB chunks. The last chunk may be smaller.
3. **Archive Format:** All output must be appended to the file specified as the second command-line argument. The archive format for each chunk is:
   - Magic Bytes (4 bytes): `0xDE 0xAD 0xBE 0xEF` (Big-endian)
   - Path Length (2 bytes, unsigned integer, Big-endian): Length of the relative file path.
   - Path (variable length): The relative file path string (e.g., `libs/math.so`). Do not include the null terminator.
   - Chunk Index (4 bytes, unsigned integer, Big-endian): 0-indexed chunk number for the file.
   - Data Length (4 bytes, unsigned integer, Big-endian): Size of the chunk payload in bytes.
   - Payload (variable length): The actual file data.
4. **Concurrency & Locking:** Another background service may be writing metadata to the archive file simultaneously. You MUST acquire an exclusive `flock()` on the archive file before writing each complete chunk record (header + payload), and release it immediately after.
5. **Fixture:** We have provided a stripped, compiled binary at `/app/validator` which verifies the integrity of the custom archive format. You can use it to test your output: `/app/validator /path/to/archive.bin`.

Write and compile the C program. Run it on `/home/user/artifacts` and output to `/home/user/repository.bin`. Your solution will be evaluated based on the fraction of correctly packed, non-looping files in the repository. Ensure your code is performant and successfully bypasses symlink traps.