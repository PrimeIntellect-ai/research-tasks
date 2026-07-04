You are acting as a technical writer organizing a fragmented documentation repository. You have a set of custom-compressed text files scattered throughout `/home/user/docs/`. 

Your task is to write a C program to decompress specific files safely, and then use shell commands to find and process the right files.

1. Write a C program at `/home/user/rle_processor.c` that takes two arguments: an input file path and an output file path.
2. The program must read the input file, which is compressed using a custom Run-Length Encoding (RLE) format. The format consists of pairs of `<integer><character>` (e.g., `3A2b1C` decompresses to `AAAbbC`). The integer can be multi-digit.
3. The program must append the decompressed string to the output file. 
4. **Important**: Because other background processes might be accessing the output file, your C program MUST acquire an exclusive file lock on the output file (using `flock()` or `fcntl()`) before appending data, and release it after writing.
5. Compile your C program to `/home/user/rle_processor`.
6. Use metadata-based file search (e.g., `find`) to locate all `.rld` (Run-Length Document) files in `/home/user/docs/` that have been modified within the last 24 hours. Ignore older files.
7. Run your compiled program on each found file, appending the decompressed contents to `/home/user/master_doc.txt`.

Ensure the final `/home/user/master_doc.txt` only contains the decompressed contents of the recently modified files.