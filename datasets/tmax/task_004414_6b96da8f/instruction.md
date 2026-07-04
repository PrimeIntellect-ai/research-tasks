You are assisting a technical writer who is trying to archive a massive, poorly organized documentation repository. The repository contains many nested directories, text files, and symlinks. Unfortunately, a previous automated tool created symbolic links that point back to parent directories, creating infinite loops. Standard archiving tools keep getting stuck or crashing. 

The publishing system requires the documentation to be merged, custom-compressed, and split into small chunks. 

Your task is to write a C program that performs this specialized archiving. The program should be compiled to `/home/user/archive_docs` and, when executed, read from `/home/user/docs_input` and write to `/home/user/docs_output`.

Here are the exact requirements for your C program:

1. **Safe Traversal & Resolution**: 
   - Traverse the `/home/user/docs_input` directory.
   - Look for all files ending in `.txt`.
   - You must follow symlinks, but **you must detect and skip circular symlinks or previously visited files/directories** to prevent infinite loops (e.g., by tracking visited inodes).
   - Only process each unique regular file once, even if multiple valid symlinks point to it.

2. **Merging**:
   - Order the resolved, unique `.txt` files strictly alphabetically by their absolute resolved target file path.
   - Merge the contents of these files in that alphabetical order.

3. **Custom Compression (RLE)**:
   - Apply a simple Run-Length Encoding (RLE) to the merged text stream.
   - For any sequence of consecutive identical characters (including whitespace and newlines), output the count as a single unsigned byte (1-255), followed by the character itself (1 byte). 
   - For example, "AABBB" becomes `[0x02, 'A', 0x03, 'B']`.
   - If a sequence exceeds 255 identical characters, split it. For example, 260 'A's becomes `[0xFF, 'A', 0x05, 'A']`.

4. **Chunking**:
   - Write the compressed byte stream into `/home/user/docs_output/` as a series of chunk files named `chunk_0000.dat`, `chunk_0001.dat`, `chunk_0002.dat`, etc.
   - Every chunk must be exactly 512 bytes in size, except for the final chunk, which contains the remaining bytes.

5. **Manifest**:
   - Create a text file at `/home/user/docs_output/manifest.txt`.
   - This file must list the absolute paths of the target `.txt` files that were successfully included in the archive, sorted alphabetically, one path per line.

**Constraints:**
- Use C as your primary programming language for the tool.
- Ensure the output directory `/home/user/docs_output/` exists or is created by your program.
- You have GCC available to compile your code.

Write the code, compile it, and run it so that the final chunks and manifest are generated in `/home/user/docs_output/`.