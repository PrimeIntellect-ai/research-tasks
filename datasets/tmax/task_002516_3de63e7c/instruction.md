You are an artifact manager tasked with curating a binary repository. The repository is located at `/home/user/repo/` and contains several gzip-compressed artifacts (`*.gz`). Unfortunately, a previous automated process created recursive symlinks in this directory, causing standard traversal tools to get stuck in infinite loops if they blindly follow symlinks.

Your objective is to safely extract metadata, rename these artifacts based on the checksum of their *uncompressed* contents, and generate a final manifest.

Perform the following steps:

1. Write a C program named `/home/user/zsha256.c`. This program must:
   - Take a single file path as a command-line argument.
   - Open the file as a gzip compressed stream (using `zlib`).
   - Read the *uncompressed* contents of the stream.
   - Compute the SHA-256 hash of the uncompressed data (using OpenSSL's `libcrypto`).
   - Print *only* the lowercase hexadecimal SHA-256 string to standard output, followed by a newline.
   - Compile it to an executable named `/home/user/zsha256`.

2. Safely traverse the `/home/user/repo/` directory to find all regular `*.gz` files. You must avoid falling into symlink infinite loops (do not follow symlinks).

3. For each regular `.gz` file found:
   - Run your `zsha256` tool on it to get the uncompressed payload's hash.
   - Copy the original compressed file to a new curation directory at `/home/user/curated/` with the new name `<hash>.gz`. (e.g., if the hash is `abc...123`, the file should be `/home/user/curated/abc...123.gz`).
   - Append an entry to `/home/user/curated/manifest.txt` in the exact format: `<hash> <relative_path_from_repo>` (e.g., `abc...123 subdir/artifact.gz`). 

4. Sort the lines in `/home/user/curated/manifest.txt` alphabetically and save the sorted version back to `/home/user/curated/manifest.txt`.

Ensure `/home/user/curated/` is created before copying files. You can use standard Linux utilities alongside your C program to accomplish the traversal, renaming, and manifest generation.

Required libraries `zlib1g-dev` and `libssl-dev` are already available on the system. You may compile with: `gcc -o zsha256 zsha256.c -lz -lcrypto`