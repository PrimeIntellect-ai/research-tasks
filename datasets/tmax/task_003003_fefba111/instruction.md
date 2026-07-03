You are an AI assistant helping a storage administrator manage disk space and analyze application logs. The log rotation script has been saving logs in a custom Run-Length Encoding (RLE) format to save space, but we need to extract specific error events.

Your task:
1. Write a Rust program at `/home/user/decode_rle.rs` and compile it to `/home/user/decode_rle`. The program must take a single file path as a command-line argument, read the file as a custom RLE binary format, and print the decoded ASCII text to standard output.
   - **RLE Format Specification**: The binary file consists of pairs of bytes. The first byte in a pair is the count (`u8`), and the second byte is the ASCII character (`u8`). For example, the bytes `[0x03, 0x41, 0x02, 0x42]` represent the string "AAABB".
2. Use standard shell tools (like `find`, `xargs`, `grep`, redirection, and piping) to recursively traverse the directory `/home/user/storage_logs/` and find all files ending with `.rle`.
3. Process all found `.rle` files using your Rust decoder. Filter the decoded output to keep only the lines that contain the exact string `CRITICAL_OOM`.
4. Sort the filtered lines alphabetically and save the final output to `/home/user/oom_events.log`.
5. Finally, create a symbolic link at `/home/user/latest_incident` that points to `/home/user/oom_events.log`.

Ensure the Rust program correctly handles the binary parsing and that your shell commands properly chain the standard output and redirection.