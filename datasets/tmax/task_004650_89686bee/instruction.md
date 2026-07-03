You are acting as an artifact manager for a secure binary repository. A fragmented software artifact has been uploaded to your staging directory, but the chunks arrived out of order.

Your task is to reassemble these chunks into a valid archive based on a provided manifest, verify its integrity, and extract its contents. 

Here are the requirements:
1. You will find the staging directory at `/home/user/staging/`. It contains several binary chunk files and a configuration file named `manifest.txt`.
2. The `manifest.txt` file specifies the correct order to merge the chunks. Each line dictating a chunk's order starts with the string `CHUNK: ` followed by the filename (e.g., `CHUNK: chunk_X.bin`).
3. Write a C program at `/home/user/merger.c` that parses `/home/user/staging/manifest.txt`. The program must read each specified chunk file in the exact order listed and append its binary contents into a single output file at `/home/user/staging/assembled.tar.gz`.
4. Compile your C program and run it to perform the merge.
5. After merging, verify the archive's integrity (it is a gzip-compressed tar archive). 
6. Extract the contents of `/home/user/staging/assembled.tar.gz` into the directory `/home/user/release/`.

Ensure that you handle file paths correctly inside your C program (the chunks are located in `/home/user/staging/`). You may use standard shell commands to compile your code and extract the archive, but the merging logic and configuration parsing must be implemented in C.