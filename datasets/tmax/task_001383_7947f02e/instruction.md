You are tasked with helping a backup administrator archive metadata from a large, corrupted audio backup directory. 

The directory `/app/backup_tree` contains thousands of subdirectories, some `.wav` files, and many symlinks. Due to a previous script error, some symlinks form infinite loops (e.g., `dirA/link -> ../dirA`). 

Your objective is to write a high-performance C program, saved at `/home/user/extractor.c`, that does the following:
1. Recursively traverses the `/app/backup_tree` directory starting from the root.
2. Robustly detects and avoids infinite symlink loops (e.g., by tracking visited device/inode pairs).
3. Identifies all regular files ending with the `.wav` extension.
4. Uses memory-mapped I/O (`mmap`) to read each `.wav` file.
5. Parses the RIFF/WAV format to locate a custom chunk with the ID `UTF1`.
6. Extracts the payload of the `UTF1` chunk, which contains text encoded in UTF-16LE.
7. Converts the UTF-16LE text to UTF-8.
8. Uses zlib to write the converted UTF-8 text into a single gzip-compressed stream saved at `/home/user/metadata.gz`. The output for each file should be a single line containing the filename (just the basename) followed by a colon, a space, and the UTF-8 text.

Additionally, a sample audio file is provided at `/app/speech.wav` for you to inspect the structure and test your parsing logic.

Requirements:
- Your code must be written in C and must compile with `gcc -O3 -lz /home/user/extractor.c -o /home/user/extractor`.
- The program must accept the target directory as its first command-line argument, and the output gzip file path as its second argument. Example: `./extractor /app/backup_tree /home/user/metadata.gz`.
- Performance is critical. We will evaluate your solution's speed against a strict runtime metric threshold. The traversal, parsing, and compression must be heavily optimized.

Create the program, ensure it compiles, and test it against the `/app/backup_tree` directory to generate the final `/home/user/metadata.gz` file.