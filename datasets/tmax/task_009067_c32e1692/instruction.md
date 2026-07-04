You are assisting a technical writer in migrating legacy documentation assets into a modern Markdown-based static site generator. 

The legacy documentation consists of custom binary bundle files (`.bin`) stored in `/home/user/legacy_docs/`. Each binary file contains a single documentation page and its intended relative output path.

You need to write a Go program at `/home/user/doc_converter.go` that reads these binary bundles, extracts the contents, converts them, and saves them to the proper directory structure. Because there are many files in the real system, your Go program must process the files concurrently using goroutines.

Here are the specific requirements for your Go program:

1. **Binary Format Parsing**:
   Each `.bin` file in `/home/user/legacy_docs/` follows this exact binary structure:
   - **Offset 0-3**: Magic bytes `DOCB` (ASCII).
   - **Offset 4-7**: A 32-bit unsigned integer (Little Endian) representing the length of the relative file path ($L$).
   - **Offset 8 to 8+$L$**: The relative file path as an ASCII string (e.g., `api/v1/auth.md`).
   - **Offset 8+$L$ to EOF**: The file content, which is Base64 encoded.

2. **Format Conversion & Path Manipulation**:
   - Extract the relative path.
   - Decode the Base64 payload into plain text Markdown.
   - Reconstruct the full output path by appending the extracted relative path to `/home/user/docs_out/`. 
   - Create any necessary parent directories for the output path.
   - Write the decoded Markdown text to the destination file.

3. **Concurrency and File Locking**:
   - Process the `.bin` files concurrently.
   - As each file finishes successfully, the goroutine must append a single line to `/home/user/docs_out/conversion.log`.
   - The log format must be exactly: `[SUCCESS] <filename.bin> -> <relative/path.md>` (e.g., `[SUCCESS] doc1.bin -> intro.md`).
   - **Critical**: Because multiple goroutines will be writing to `conversion.log` concurrently, you *must* use OS-level file locking (e.g., `syscall.Flock` or `golang.org/x/sys/unix`) to acquire an exclusive lock on the log file before appending the line, and release it afterward, to prevent interleaved writes.

4. **Execution**:
   - Write the complete, runnable Go code to `/home/user/doc_converter.go`.
   - Run your program to process all files in `/home/user/legacy_docs/`.