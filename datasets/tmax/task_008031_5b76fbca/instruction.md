You are acting as a technical writer organizing documentation for a legacy system. 

The engineering team has provided you with an archive located at `/home/user/docs_archive.zip`. This archive contains several nested tarballs (`part1.tar.gz`, `part2.tar.gz`), which in turn contain documentation files in a proprietary binary format with the extension `.bdoc`.

Your goal is to extract these files, parse them using a C++ program you must write, and convert them into a single Markdown file at `/home/user/compiled_docs.md`. Because there are usually thousands of these files (though this test only has a few), you need to process them concurrently, which requires your C++ program to use file locking to prevent data corruption.

Here are the specifications for the `.bdoc` binary format (Little-Endian):
1. **Magic Number:** The first 4 bytes are exactly the ASCII characters `BDOC`.
2. **Title Length:** The next 4 bytes are an unsigned 32-bit integer representing the length of the title string.
3. **Title:** The title string in ASCII (not null-terminated, length exactly as specified above).
4. **Content Length:** The next 4 bytes are an unsigned 32-bit integer representing the length of the content string.
5. **Content:** The content string in ASCII (not null-terminated).

Your tasks:
1. Extract the nested archives completely so all `.bdoc` files are accessible.
2. Write a C++ program at `/home/user/bdoc_parser.cpp`. The program must:
   - Take the input `.bdoc` file path as `argv[1]`.
   - Parse the binary file according to the specifications.
   - Append the extracted documentation to `/home/user/compiled_docs.md` in the following exact format:
     ```markdown
     # [Title]

     [Content]
     ---
     ```
   - **Crucially:** Open `/home/user/compiled_docs.md` and use `flock()` (with `LOCK_EX`) on its file descriptor before writing, and unlock it afterward, ensuring thread-safe appends during concurrent execution.
3. Compile your C++ program to `/home/user/bdoc_parser`.
4. Run your compiled program concurrently on all extracted `.bdoc` files using standard bash tools (e.g., `find` combined with `xargs -P 4` or `parallel`).
5. After all files are processed, sort the blocks in `/home/user/compiled_docs.md` alphabetically by Title to ensure a deterministic final output. Wait, sorting markdown blocks in bash can be tricky. Instead, just write another short command or script to read `compiled_docs.md` and sort the blocks by title, outputting to `/home/user/final_docs.md`. (A block starts with `# [Title]` and ends with `---`).