You are an AI assistant helping a technical writer automate their documentation workflow. The writer receives draft documents from legacy systems encoded in `ISO-8859-1`. They need a Linux background daemon written in C that watches a "drop folder", processes these legacy text files safely, converts their encoding, and archives them into a single structured binary file.

Your task is to write, compile, and run this C program. 

**Requirements for the C program (`/home/user/doc_watcher.c`):**

1. **Directories & Watching:**
   - Watch the directory `/home/user/incoming_docs/` for new files using `inotify`. You should listen for `IN_CLOSE_WRITE` and `IN_MOVED_TO` events.
   - You must create `/home/user/incoming_docs/` and `/home/user/archive/` before running the program.

2. **File Locking & Reading:**
   - When a file is detected, open it and acquire an exclusive lock using `flock()` to prevent race conditions.
   - Read the contents of the file. The legacy system guarantees that the very first line (up to the first `\n`) is the Document Title, and everything after the `\n` is the Document Content.

3. **Character Encoding Conversion:**
   - The incoming files are strictly encoded in `ISO-8859-1`.
   - Use the `iconv` library in C to convert both the Title and the Content into `UTF-8`. (Do not include the `\n` from the title line in the converted Title string).

4. **Binary Archiving:**
   - Append the converted document to `/home/user/archive/docs.bin`.
   - Before writing, acquire an exclusive lock on `docs.bin` to allow safe concurrent appends (in case multiple writer processes were to run).
   - Write the record in the following strict binary format:
     - **Magic Bytes:** 2 bytes, `0xCA 0xD0` (representing `DOCA` in little-endian).
     - **Title Length:** 4 bytes, `uint32_t` in little-endian (length of the UTF-8 title in bytes).
     - **Title:** Variable length, the UTF-8 encoded title (no null-terminator).
     - **Content Length:** 4 bytes, `uint32_t` in little-endian (length of the UTF-8 content in bytes).
     - **Content:** Variable length, the UTF-8 encoded content.
   - After writing, release the lock and close both files. Finally, delete the original text file from `incoming_docs`.

**Execution & Verification:**
1. Write the code to `/home/user/doc_watcher.c`.
2. Compile it to `/home/user/doc_watcher` (e.g., `gcc -o /home/user/doc_watcher /home/user/doc_watcher.c`).
3. Start the compiled program in the background (e.g., `./doc_watcher &`).
4. To test your setup, manually create a file `/home/user/incoming_docs/test1.txt`. Ensure it is encoded in `ISO-8859-1` and contains exactly:
   Line 1: `Café Draft`
   Line 2+: `Résumé of the completely updated system.`
   (Hint: You can use `iconv` in the shell to generate this test file).
5. Verify that `docs.bin` is generated correctly and `test1.txt` is deleted. Leave the background process running so our automated test suite can drop further files to evaluate it.